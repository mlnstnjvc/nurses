from django import forms


class ParamForm(forms.Form):
    id = forms.CharField(
        max_length=20)
    value = forms.FloatField()
    text = forms.CharField(
        widget = forms.Textarea)
    
