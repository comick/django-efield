Django editable field
=====================

Make template fields editable in place using some reflection tricks.
Make sure you include jQuery in your template.
Tested with Django 1.2 and 1.3, may stop working in future since use some internal "private" stuff.

Usage
-----

1. Enable efield to your project installed apps

2. On top of template files you want to use efield in, add :

`{% load efield %}`

3. When you want a filed to be editable use:

`{% efield obj.field %}`

instead of:

`{{ obj.field }}`

4. Enjoy and contribute.

Notes
-----

Django authentication model is based on models.
Projects exist to extend the authentication model on a per-object basis.

Meanwhile efiled make it possible by implementing a 

`get_owner()`

method inside your models.

Always use RequestContext instead of Context when dealing with templates using efield bounties.
It needs the user.

TODO
----

To much of the model is revealed to the user, try to find a better solution for reflection tips.
Heavely untested on some widget fields.
No security check at all, possible vulnerability.

The code is about the reflection trick, the TODOs are the tedious part i never completed since the project was dropped.
Pull, fork, or whatever you want if you think it's useful.

AUTHOR
------

Michele "comick" Comignano <comick@inventati.org>
