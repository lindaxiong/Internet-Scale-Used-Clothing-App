from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

# Create your views here.

def homepage(request):
    return HttpResponse("Basic Homepage")

#TODO: Error Checking - shouldn't be able to do a GET method when creating - SEE: DECORATORS!!

@require_POST()
#TODO: Return JSON with the USER ID so you can use it.
def create_user(request):
    #Ensure it's a POST request - need info to populate fields.
    if request.method == "POST":
        # Use the request data to populate the form.
        form = UserForm(request.POST)
        # If the form is valid ...
        if form.is_valid():
            #save the instance
            form.save()
            # Return user ID JSON
	    response = {}
	    response['userID'] = form.pk
	    return JsonResponse(response)		
#TODO: Error Checking: ID not found, raise problem if form is NOT valid.
	else:
	    

def get_user(request, user_id):
    if request.method == "GET":
        user_instance = User.object.get(pk=user_id)
        #JSON Response requires a dictionary input
        #TODO: Think about what fields you *specifically* want to return. Must be a dictionary.
        return JsonResponse(model_to_dict(user_instance))

def edit_user(request, user_id):
    if request.method == "POST":
        # Finds the specific instance of the user
        #TODO: What if ID not found?
        user_instance = User.objects.get(pk=user_id)
        #TODO: Change from resubmitting an entire form to editing single fields if necessary
        #TODO: Add restrictions for changing certain fields (not *super* relevant right now)
        user = UserForm(request.POST, instance=user_instance)
        #TODO: Add JSON response indicating success
        if user.is_valid():
            user.save()

#TODO: Repeat above steps on the following - should be near-identitical
@require_POST()
def create_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid:
            form.save()
	    response = {}
            response['userID'] = form.pk
            return JsonResponse(response)


def get_item(request, item_id):
    if request.method == "GET":
        item_instance = Item.object.get(pk=user_id)
        return JsonResponse(model_to_dict(item_instance))

def edit_item(request, item_id):
    if request.method == "POST":
        item_instance = Item.objects.get(pk=item_id)
        item = ItemForm(request.POST, instance=user_instance)
        if item.is_valid():
            item.save()
