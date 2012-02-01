# -*- coding: utf-8 -*-
'''Editable layout tags to create pages offering rapid user interaction.'''
from django import template
from django.db import models
from django.template.context import Context
from django.forms.models import ModelForm
from django.forms.models import fields_for_model
from django.db.models import ImageField

register = template.Library()
# TODO per tutti controllare chela group key sia una stringa di lettere tutte piccole etc etc
@register.tag(name='efield_save_all')
def do_efield_save_all(parse, token):    
    '''
    Show a button to save all the editable fields making part 
    of the same group whose contents haven't been saved yet.

    If you use it without parameters, the save all button will 
    regard any editable field in the template::

        {% efield_save_all %}

    Elsewhere you can specify a key identifying the group whose 
    editable fields will be saved by this button::

        {% efield_save_all "group_key" %}
    '''
    args = token.split_contents()
    
    if len(args) == 1:
        return EfieldSaveAllNode()
    elif len(args) == 2:
        return EfieldSaveAllNode(args[1])
    else:
        raise template.TemplateSyntaxError, "%r tag admits one argument" % args[0] 


@register.tag(name='efield')
def do_efield(parse, token):
    '''
    Show an editable field, that is an object field that an user 
    with proper rights could edit in place.

    Use it specifying any field of an object in the template 
    context like in following example::

        {% efield person.name %}

    or if you want specify a group for save all requests::

        {% efield person.name group_key %}
        
    Assuming "person" being a relational object in template context.
    
    If the user hasn't proper rights the editable field will be 
    shown as if was used::
    
        {{ object.field }}
        
    Be sure to use a RequestContext in your view or edfield 
    won't be able to check for user permissions.
    '''
    args = token.split_contents()
    if len(args) == 2:
        return EfieldNode(args[1])
    # TODO controllare che group sia alfanumerico
    elif len(args) == 3:
        if args[2][0] == '"':
            try:
                options = eval(args[2][1:-1], {}, {})
                if not isinstance(options, dict):
                    raise TypeError
                return EfieldNode(args[1], options=options)
            except Exception:
                raise template.TemplateSyntaxError, "%r tag requires options to be a Python dict" % args[0]
        else:
            return EfieldNode(args[1], group_key=args[2])
    # TODO caso con 4 distinguere se e un option o un grouppo
    else:
        raise template.TemplateSyntaxError, "%r tag requires a one to three arguments" % args[0]

class EfieldNode(template.Node):
    ef_id = 1
    def __init__(self, field_name, group_key='', options={}):
        self.field_var = template.Variable(field_name)
        self.tokens = field_name.split('.')
        self.field_name = self.tokens.pop()
        self.group_key = group_key
        self.options = options
    def render(self, context):
        try:
            obj = context
            for token in self.tokens:
                try:
                    obj = obj[token]
                except TypeError:
                    obj = obj[int(token)]
            field_val = self.field_var.resolve(context)
            assert(isinstance(obj, models.Model))
            #if not context['user'].is_authenticated() or context['user'] != obj.get_owner():
            #    return field_val
        except Exception as e:
            return e

        widget = fields_for_model(type(obj), [self.field_name])[self.field_name].widget

        if 'input_classes' in self.options:
            widget.attrs['class'] = self.options['input_classes']

        class PartialForm(ModelForm):
            class Meta:
                model = type(obj)
                fields = [self.field_name]
                widgets = {
                    self.field_name: widget
                }
        
        c = Context({'value': field_val,
                     'model': obj.__class__.__module__ + '.' + obj.__class__.__name__,
                     'object_id': obj.id,
                     'ef_id': str(EfieldNode.ef_id),
                     'name': self.field_name,
                     'form': PartialForm(instance=obj)
        })
        for opt_key, opt_val in self.options.items():
            if opt_key == 'jstrigger':
                c[opt_key] = opt_val
            else:
                pass
                # Opzione sconosciuta, che fare???
        EfieldNode.ef_id += 1
        field_type = obj._meta.get_field_by_name(self.field_name)[0]
        if self.group_key:
            c['group_key'] = self.group_key
        if isinstance(field_type, ImageField):
            t = template.loader.get_template('efield_image.html')
        else:
            t = template.loader.get_template('efield.html')
        return t.render(c)            


class EfieldSaveAllNode(template.Node):
    def __init__(self, group=None):
        self.group = group
    def render(self, context):
        t = template.loader.get_template('efield_save_all.html')
        return t.render(Context({'group': self.group}))       
