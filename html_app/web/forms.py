from django import forms

class UserCreationForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=100)
