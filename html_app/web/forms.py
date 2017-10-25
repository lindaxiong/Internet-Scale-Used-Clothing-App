from django import forms

#Forms for user creation, logging in, and listing creation. max_length is based off criteria specified in uc_app's models. 

class UserCreationForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=100)

class LogInForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=100)

class ListingForm(forms.Form):
    item_name = forms.CharField(max_length=30)
    item_price = forms.DecimalField(max_digits=10, decimal_places=2)
    #seller field was put here to be pre-filled, not the optimal solution 
    seller = forms.CharField(max_length=30)
    brand = forms.CharField(max_length=100)
    description = forms.CharField()
    image_url = forms.URLField(max_length=1000)
    ITEM_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('OS', 'One Size'),
        ('Other', 'Other')
    )
    item_size = forms.ChoiceField(choices=ITEM_SIZES)
    ITEM_TYPES = (
        ('Top', 'Top'),
        ('Bottom', 'Bottom'),
        ('Dress', 'Dress'),
        ('Footwear', 'Footwear'),
        ('Accessory', 'Accessory'),
        ('Other', 'Other')
    )
    item_type = forms.ChoiceField(choices = ITEM_TYPES)
