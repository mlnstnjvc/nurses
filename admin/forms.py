from django import forms
from django.utils.translation import ugettext as _
from djangular.forms.angular_model import NgModelFormMixin

class NurseForm(NgModelFormMixin, forms.Form):
    first_name = forms.CharField(
        label = _("First Name"),
        required = True)
    last_name = forms.CharField(
        label = _("Last Name"),
        required = True)
    experienced = forms.BooleanField(
        label = _("Experienced"))

    def __init__(self, *args, **kwargs):
        kwargs.update(scope_prefix='nurse')
        super(NurseForm, self).__init__(*args, **kwargs)
