from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.exceptions import *
from django.views.decorators.http import *
import json

# Create your views here.

@require_POST
def create_user(request):
    #Ensure it's a POST request - need info to populate fields.
    if request.method == "POST":
        # Use the request data to populate the form.
        form = UserForm(request.POST)
        # If the form is valid ...
        response = {}
        if form.is_valid():
            #save the instance
            form.save()
            # Return user ID JSON
            response = JsonResponse({'userID':form.pk})
        else:
            # Return an error response if invalid
            message = "Invalid user form submitted!"
            response = JsonResponse({'status':'false', 'message':message}, status=500)
        return response

@require_GET
def get_user(request, user_id=0):
    if request.method == "GET":
        try:
            user = User.object.get(pk=user_id)
            response = JsonResponse(model_to_dict(user))
        except ObjectDoesNotExist:
            message = "Object not found!"
            response = JsonResponse({'status':'false', 'message':message}, status=404)
        #JSON Response requires a dictionary input
        return response

@require_POST
def edit_user(request, user_id=0):
    if request.method == "POST":
        # Finds the specific instance of the user
        try:
            user_instance = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            message = "Object not found!"
            return JsonResponse({'status':'false', 'message':message}, status=500)
        user = UserForm(request.POST, instance=user_instance)
        if user.is_valid():
            user.save()
            return JsonResponse({'userID':user.pk})
        else:
            message = "Invalid change."
            return JsonResponse({'status':'false', 'message':message}, status=500)

@require_POST
def create_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        response = {}
        if form.is_valid():
            #save the instance
            form.save()
            # Return user ID JSON
            response = JsonResponse({'itemID':form.pk})
        else:
            # Return an error response if invalid
            message = "Invalid item form submitted!"
            response = JsonResponse({'status':'false', 'message':message}, status=500)
        return response

@require_GET
def get_item(request, item_id=0):
    if request.method == "GET":
        try:
            item = Item.object.get(pk=user_id)
            response = JsonResponse(model_to_dict(item))
        except ObjectDoesNotExist:
            message = "Item not found!"
            response = JsonResponse({'status':'false', 'message':message}, status=500)
        #JSON Response requires a dictionary input
        return response

@require_POST
def edit_item(request, item_id=0):
    if request.method == "POST":
        # Finds the specific instance of the user
        try:
            item_instance = Item.objects.get(pk=item_id)
        except ObjectDoesNotExist:
            message = "Object not found!"
            return JsonResponse({'status':'false', 'message':message}, status=500)
        item = ItemForm(request.POST, instance=item_instance)
        if item.is_valid():
            item.save()
            return JsonResponse({'itemID':item.pk})
        else:
            message = "Invalid change."
            return JsonResponse({'status':'false', 'message':message}, status=500)
