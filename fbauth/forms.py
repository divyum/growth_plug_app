from django import forms

# our new form
class UpdateForm(forms.Form):
    # name = forms.CharField(required=False)
    # email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)