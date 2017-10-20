from django import forms
from .models import *
from django.forms import ModelForm

#Forms are a short-cut for rendering information "forms" on a web page that can be easily returned in a POST request.
#These are "Model Forms" which specifically update exisiting models or make new ones based on Model definitions.
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_price', 'seller', 'buyer', 'brand', 'description', 'item_size', 'item_type']

class AuthForm(forms.ModelForm):
    class Meta:
        model = Authenticator
        fields = ['user_id', 'authenticator']
