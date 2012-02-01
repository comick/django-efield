from django.http import HttpResponse
from string import join
from django.forms.models import ModelForm

def save(request):
    if request.method != 'POST' or not request.is_ajax():
        return HttpResponse(status=501)
    #if not request.user.is_authenticated():
    #    return HttpResponse('You should be logged in.', status=403)
    field_name = request.POST['field']
    new_value = request.POST[field_name]
    tokens = request.POST['model'].split('.')
    model_name = tokens.pop()
    module = __import__(join(tokens, '.'), globals(), locals(), fromlist=model_name)
    model = getattr(module, model_name)
    obj = model.objects.get(id=request.POST['object_id'])
    #if request.user != obj.get_owner():
    #    return HttpResponse('You should be the owner.', status=403)
    class PartialForm(ModelForm):
            class Meta:
                model = type(obj)
                fields = [field_name]
    form = PartialForm({field_name: new_value}, instance=obj)
    try:
        form.save()
        return HttpResponse(getattr(obj, field_name))
    except ValueError as error:# TODO un errore generico, noi lo vogliamo aprticolare
        return HttpResponse(error, status=406)
