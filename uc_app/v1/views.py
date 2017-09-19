from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

def homepage(request):
    return HttpResponse("Basic Homepage")

def create_user(request):
    #Ensure it's a POST request - need info to populate fields.
    if request.method == "POST":
        # Use the request data to populate the form.
        form = UserForm(request.POST)
        # If the form is valid ...
        if form.is_valid():
            #save the instance
            form.save()

def access_user(request, user_id):
    if request.method == "POST":
        user_instance = User.objects.get(pk=user_id)
        user = UserForm(request.POST, instance=user_instance)
        if user.is_valid():
            user.save()
    if request.method == "GET":
        user_instance = User.object.get(pk=user_id)
        #JSON Response requires a dictionary input
        return JsonResponse(model_to_dict(user_instance))


def create_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid:
            form.save()

def access_item(reuqest, item_id):
    if request.method == "POST":
        item_instance = Item.objects.get(pk=item_id)
        item = ItemForm(request.POST, instance=user_instance)
        if item.is_valid():
            item.save()
    if request.method == "GET":
        item_instance = Item.object.get(pk=user_id)
        return JsonResponse(model_to_dict(item_instance))
