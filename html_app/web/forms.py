from django import forms

#Froms for user creation and logging in. max_length is based off criteria specified in uc_app's models. 

class UserCreationForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=100)

class LogInForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=100)
