from django.shortcuts import render
from v1.models import *
from v1.forms import *
from django.forms import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.exceptions import *
from django.views.decorators.http import *
import json

# Create your views here.

def create_user(request):
    #Ensure it's a POST request - need info to populate fields.
    if request.method == "POST":
        # Use the request data to populate the form.
        form = UserForm(request.POST)
        # If the form is valid ...
        response = {}
        if form.is_valid():
            #save the instance
            saved_form = form.save()
            # Return user ID JSON
            response = JsonResponse({'userID':saved_form.pk})
        else:
            # Return an error response if invalid
            response = HttpResponse(form.errors.as_json(), content_type="application/json", status=500)
        return response
    else:
        message = "Expected POST request to create user object - other type of request recieved"
        return JsonResponse({'status':'false','message':message}, status=500)

def get_user(request, user_id=0):
    if request.method == "GET":
        try:
            user = User.objects.get(pk=user_id)
            response = JsonResponse(model_to_dict(user))
        except ObjectDoesNotExist:
            message = "User objecat at ID " + str(user_id) + " not found!"
            response = JsonResponse({'status':'false', 'message':message}, status=500)
        #JSON Response requires a dictionary input
        return response
    else:
        message = "Expected GET reqeust to retrieve user object - other type of request recieved"
        return JsonResponse({'status':'false','message':message}, status=500)

def edit_user(request, user_id=0):
    if request.method == "POST":
        # Finds the specific instance of the user
        try:
            user_instance = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            message = "User at ID " + str(user_id) + " not found!"
            return JsonResponse({'status':'false', 'message':message}, status=500)
        user = UserForm(request.POST, instance=user_instance)
        if user.is_valid():
            user.save()
            return JsonResponse({'userID':user.pk})
        else:
            response = HttpResponse(user.errors.as_json(), content_type="application/json", status=500)
            return response
    else:
        message = "Expected POST request to modify user object - other type of request recieved"
        return JsonResponse({'status':'false','message':message}, status=500)

def delete_user(request, user_id=0):
    try:
        user_instance = User.objects.get(pk=user_id)
        user_instance.delete()
        return JsonResponse({'deleted':'True'})
    except ObjectDoesNotExist:
        message = "User at ID " + str(user_id) + " not found! Deletion failed."
        return JsonResponse({'status':'false', 'message':message}, status=500)


def create_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        response = {}
        if form.is_valid():
            #save the instance
            saved_form = form.save()
            # Return user ID JSON
            response = JsonResponse({'itemID':saved_form.pk})
        else:
            # Return an error response if invalid
            response = HttpResponse(form.errors.as_json(), content_type="application/json", status=500)
        return response
    else:
        message = "Expected POST request to create item objet - other type of request recieved"
        return JsonResponse({'status':'false','message':message}, status=500)

def get_item(request, item_id=0):
    if request.method == "GET":
        try:
            item = Item.objects.get(pk=item_id)
            response = JsonResponse(model_to_dict(item))
        except ObjectDoesNotExist:
            message = "Item at ID " + str(item_id) + " not found!"
            response = JsonResponse({'status':'false', 'message':message}, status=500)
        #JSON Response requires a dictionary input
        return response
    else:
        message = "Expected GET request to retrieve item object - other type of request recieved"
        return JsonResponse({'status':'false','message':message}, status=500)

def edit_item(request, item_id=0):
    if request.method == "POST":
        # Finds the specific instance of the user
        try:
            item_instance = Item.objects.get(pk=item_id)
        except ObjectDoesNotExist:
            message = "Object at ID " + str(item_id) + " not found!"
            return JsonResponse({'status':'false', 'message':message}, status=500)
        item = ItemForm(request.POST, instance=item_instance)
        if item.is_valid():
            item.save()
            return JsonResponse({'itemID':item.pk})
        else:
            response = HttpResponse(item.errors.as_json(), content_type="application/json", status=500)
            return response
    else:
        message = "Expected POST request to modify item object - other type of request recieved"
        return JsonResponse({'status':'false','message':message}, status=500)

def delete_item(request, item_id=0):
    try:
        user_instance = Item.objects.get(pk=item_id)
        user_instance.delete()
        return JsonResponse({'deleted':'True'})
    except ObjectDoesNotExist:
        message = "User at ID " + str(item_id) + " not found!"
        return JsonResponse({'status':'false', 'message':message}, status=500)
