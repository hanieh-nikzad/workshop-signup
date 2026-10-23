from django import forms


class RegistrationForm(forms.Form):
    name = forms.CharField(label="نام", max_length=100)
    email = forms.EmailField(label="ایمیل")