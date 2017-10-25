from django.shortcuts import render
from .models import *
from .forms import *
from django.forms import *
from uc_app import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.exceptions import *
from django.core import serializers
from django.views.decorators.http import *
from django.contrib.auth import hashers
import os
import hmac
import json


def create_user(request):
    # Ensure it's a POST request - need info to populate fields.
    if request.method == "POST":
        # Use the request data to populate the form.
        form = UserForm(request.POST)
        # If the form is valid ...
        response = {}
        if form.is_valid():
            # save the instance
            saved_form = form.save()
            saved_form.password = hashers.make_password(form.cleaned_data['password'])
            saved_form.save()
            # Return user ID JSON
            response = JsonResponse({'userID': saved_form.pk})
        else:
            # Return a response with errors to be reported
            response = JsonResponse({'errors': form.errors})
        return response
    else:
        # Default response if not appropriate request type.
        message = "Expected POST request to create user object - other type of request recieved"
        return JsonResponse({'status': 'false', 'message': message}, status=500)


def get_user(request, user_id=0):
    if request.method == "GET":
        try:
            # Find the user instance
            user = User.objects.get(pk=user_id)
            user_serial = model_to_dict(user)
            user_serial['id'] = user.pk
            # format into the user uc into a dictionary (necessary for conversion), return as JSON
            response = JsonResponse(user_serial)
        except User.DoesNotExist:
            # If object cannot be found, relay information back with the user's ID.
            message = "User objecat at ID " + str(user_id) + " not found!"
            response = JsonResponse({'status': 'false', 'message': message}, status=500)
        # JSON Response requires a dictionary input
        return response
    else:
        # Default response if not appropriate request type.
        message = "Expected GET request to retrieve user object - other type of request received"
        return JsonResponse({'status': 'false', 'message': message}, status=500)


def edit_user(request, user_id=0):
    if request.method == "POST":
        # Finds the specific instance of the user
        try:
            user_instance = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # If the user can't be found, return the invalid ID and an error message.
            message = "User at ID " + str(user_id) + " not found!"
            return JsonResponse({'status': 'false', 'message': message}, status=500)
        # Use a uc form to re-format the request information
        user = UserForm(request.POST, instance=user_instance)
        # Check to see if the form is valid (e.g. valid changes were made)
        if user.is_valid():
            # If so, save the instance's changes and return the ID.
            saved_user = user.save()
            return JsonResponse({'userID': saved_user.pk})
        else:
            # Otherwise, format the errors in formatting as a JSON response and return it.
            # HTTP Response + json content and content_type flagged as json is a JSON Response.
            response = JsonResponse({'errors': user.errors})
            return response
    else:
        # Default message if invalid rquest type
        message = "Expected POST request to modify user object - other type of request recieved"
        return JsonResponse({'status': 'false', 'message': message}, status=500)


def delete_user(request, user_id=0):
    try:
        # Find the user - if it's found, delete the corresponding user.
        user_instance = User.objects.get(pk=user_id)
        user_instance.delete()
        return JsonResponse({'deleted': 'True'})
    except User.DoesNotExist:
        # Returns the invalid ID if not found.
        message = "User at ID " + str(user_id) + " not found! Deletion failed."
        return JsonResponse({'status': 'false', 'message': message}, status=500)


# Item methods correspond 1:1 to User methods. Refer to user methods for use-cases.

def create_item(request, username):
    if request.method == "POST":
        post_values = request.POST.copy()
        try:
            print(username)
            user_instance = User.objects.get(username=username.strip('/'))
            post_values['seller'] = user_instance.pk
        except User.DoesNotExist:
            return JsonResponse({'errors':{'seller':'problem locating you in our database!'}})
        form = ItemForm(post_values)
        response = {}
        if form.is_valid():
            saved_form = form.save()
            response = JsonResponse({'itemID': saved_form.pk})
        else:
            print(form.errors)
            response = JsonResponse({'errors': form.errors})
        return response
    else:
        message = "Expected POST request to create item objet - other type of request recieved"
        return JsonResponse({'status': 'false', 'message': message}, status=500)


def get_item(request, item_id=0):
    if request.method == "GET":
        try:
            item = Item.objects.get(pk=item_id)
            item_serial = model_to_dict(item)
            item_serial['id'] = item.pk
            response = JsonResponse(item_serial)
        except Item.DoesNotExist:
            message = "Item at ID " + str(item_id) + " not found!"
            response = JsonResponse({'status': 'false', 'message': message}, status=500)
        return response
    else:
        message = "Expected GET request to retrieve item object - other type of request recieved"
        return JsonResponse({'status': 'false', 'message': message}, status=500)


def get_item_by(request, field="", criteria=""):
    if request.method == "GET":
        items_as_json = {}
        # based on the input field, filter items.
        if field == "item_size":
            items_as_json = serializers.serialize('json', Item.objects.filter(item_size=criteria))
        elif field == "item_type":
            items_as_json = serializers.serialize('json', Item.objects.filter(item_type=criteria))
        elif field == "brand":
            items_as_json = serializers.serialize('json', Item.objects.filter(item_type=criteria))
        elif field == "item_price":
            # price defaults to finding items less than the price
            items_as_json = serializers.serialize('json', Item.objects.filter(item_type__lte=criteria))
        elif field == "description":
            items_as_json = serializers.serialize('json', Item.objects.filter(description__icontains=criteria))
        else:
            # if the field doesn't exist, this is returned.
            items_as_json = {'status': 'false', 'message': 'Not handled'}
            return JsonResponse(items_as_json, status=500)
        return HttpResponse(items_as_json, content_type="json")
    else:
        message = "Expected GET request to retrieve item object - other type of request recieved"
        return JsonResponse({'status': 'false', 'message': message}, status=500)


def edit_item(request, item_id=0):
    if request.method == "POST":
        try:
            item_instance = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            message = "Object at ID " + str(item_id) + " not found!"
            return JsonResponse({'status': 'false', 'message': message}, status=500)
        item = ItemForm(request.POST, instance=item_instance)
        if item.is_valid():
            saved_item = item.save()
            return JsonResponse({'itemID': saved_item.pk})
        else:
            response = JsonResponse({'errors': item.errors})
            return response
    else:
        message = "Expected POST request to modify item object - other type of request recieved"
        return JsonResponse({'status': 'false', 'message': message}, status=500)


def delete_item(request, item_id=0):
    try:
        item_instance = Item.objects.get(pk=item_id)
        item_instance.delete()
        return JsonResponse({'deleted': 'True'})
    except Item.DoesNotExist:
        message = "User at ID " + str(item_id) + " not found!"
        return JsonResponse({'status': 'false', 'message': message}, status=500)


def log_in(request):
    if request.method == "POST":
        try:
            user_instance = User.objects.get(username=request.POST['username'])
            if hashers.check_password(request.POST['password'], user_instance.password):
                auth = hmac.new(
                    key=settings.SECRET_KEY.encode('utf-8'),
                    msg=os.urandom(32),
                    digestmod='sha256',
                ).hexdigest()
                new_auth = AuthForm({'authenticator': auth, 'user_id': user_instance.pk})
                if new_auth.is_valid():
                    saved_auth = new_auth.save()
                    return JsonResponse({'auth_id': saved_auth.authenticator})
                # If, for some reason, the authenticator doesn't work ...
                else:
                    return JsonResponse({'errors': {'auth_error': 'Failture to create authenticator'}})
            # If the passwords don't match ...
            else:
                return JsonResponse(
                    {'errors': {'password': "Password is incorrect for the user " + user_instance.username}})
        # If the username didn't have an associated user...
        except User.DoesNotExist:
            return JsonResponse({'errors': {'username': "Username didn't match any exisiting users in our databse"}})
    # If it's not a post ...
    else:
        message = "Expected POST request to modify item object - other type of request recieved"
        return JsonResponse({'status': 'false', 'message': message}, status=500)


def log_out(request, auth_id):
    if request.method == "POST":
        try:
            auth_instance = Authenticator.objects.get(authenticator=auth_id)
            auth_instance.delete()
            return JsonResponse({
                'logout':'success'
            })
        except Authenticator.DoesNotExist:
            return JsonResponse({'errors': "Authenticator does not exist in our database!"})
    else:
        return JsonResponse({'status': 'false',
                             'message': 'Expected POST, recieved GET'
                             }, status=500)


def authenticate(request, auth_id):
    if request.method == "GET":
        try:
            auth_instance = Authenticator.objects.get(authenticator=auth_id)
            return JsonResponse({
                'logged_in': True,
                'username': auth_instance.user_id.username
            })
        # If the authenticator isn't there, user isn't logged in.
        except Authenticator.DoesNotExist:
            return JsonResponse({'logged_in': False})
    else:
        return JsonResponse({'status': 'false',
                             'message': 'Expected GET, recieved POST'
                             }, status=500)
