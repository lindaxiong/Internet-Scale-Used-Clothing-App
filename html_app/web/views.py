from django.shortcuts import render
import urllib.request
import urllib.parse
from web.forms import UserCreationForm, LogInForm, ListingForm
from django.http import *
from django.urls import *
import json
import random

EXP_API = 'http://exp-api:8000/api/v1/'


def sign_up(request):
    # resp to collect data to be returned
    resp = {}
    auth = authenticate(request)
    # check to see if the user is authenticated, returns with the username added to the response
    if auth['logged_in']:
        resp['logged_in'] = auth['username']
    if request.method == "POST":
        try:
            create_usr_req = urllib.request.Request(url=EXP_API + 'user/create/', method='POST', data=request.body)
            create_usr_json = urllib.request.urlopen(create_usr_req).read().decode('utf-8')
            cu_resp = json.loads(create_usr_json)
        except urllib.error.HTTPError:
            return render(request, 'home_page.html', {'message':{'status_message':'Something went wrong when processing your request.'}})
        # creates an empty form to render on the page
        resp['form'] = UserCreationForm()
        # if the exp app returns success as status
        if cu_resp['status'] == 'success':
            # set this as the status message in the "message"
            resp['message'] = {'status_message': 'User successfully created!'}
        else:
            # if there's already a status message, keep it
            if 'status_message' not in cu_resp['errors']:
                cu_resp['errors']['status_message'] = 'User creation failed!'
            # message will include everything in errors. (including status message)
            resp['message'] = cu_resp['errors']
    else:
        # If it's a get request just render a blank form to the page.
        resp['form'] = UserCreationForm()
    return render(request, 'signup.html', resp)


def log_in(request):
    auth = authenticate(request)
    # if the user is logged in, render the page immediately, just including message and a status message
    if auth.get('logged_in'):
        return render(request, 'login.html',
                      {'message': {'status_message': "You're already logged in as " + auth['username'] + "!"},
                       'logged_in': auth['username']})
    if request.method == "POST":
        try:
            login_request = urllib.request.Request(url=EXP_API + 'user/login/', method='POST', data=request.body)
            login_req_json = urllib.request.urlopen(login_request).read().decode('utf-8')
            login_resp = json.loads(login_req_json)
        except urllib.error.HTTPError:
            return render(request, 'home_page.html', {'message':{'status_message':'Something went wrong when processing your request!'}})
        # if the login was successful, get the authenticator and set the cookie to it.
        if login_resp['status'] == 'success':
            authenticator = login_resp['auth_id']
            response = HttpResponseRedirect(reverse('home'))
            response.set_cookie('auth_id', authenticator)
            return response
        # Otherwise, send the errors in the message (including a status message)
        else:
            form = LogInForm()
            if 'status_message' not in login_resp['errors']:
                login_resp['errors']['status_message'] = 'Login failed!'
            return render(request, 'login.html', {'form': form, 'message': login_resp['errors']})
    # If it's a GET request, just render the form.
    else:
        form = LogInForm()
    return render(request, 'login.html', {'form': form})

def create_listing(request):
    resp = {}
    auth = authenticate(request)
    # check to see if the user is authenticated, returns with the username
    if auth['logged_in']:
        resp['logged_in'] = auth['username']

    if not auth['logged_in']:
        response = HttpResponseRedirect(reverse('log-in'))
        return response
    if request.method == "POST":
        # doesn't return any error codes, don't need to try/catch
        try:
            create_listing_req = urllib.request.Request(url=EXP_API + 'item/create/'+auth['username']+'/', method='POST', data=request.body)
            create_listing_json = urllib.request.urlopen(create_listing_req).read().decode('utf-8')
            cl_resp = json.loads(create_listing_json)
        except urllib.error.HTTPError:
            return render(request, 'home_page.html', {'message':{'status_message':'Something went wrong when processing your request'}})
        # creates an empty form to render on the page
        resp['form'] = ListingForm()
        # if the exp app returns success as status
        if cl_resp['status'] == 'success':
            # set this as the status message in the "message"
            resp['message'] = {'status_message': 'Item successfully posted!'}
        else:
            # if there's already a status message, keep it
            if 'status_message' not in cl_resp['errors']:
                cl_resp['errors']['status_message'] = 'Listing creation failed!'
            # message will include everything in errors. (including status message)
            resp['message'] = cl_resp['errors']
    else:
        # If it's a get request just render a blank form to the page.
        resp['form'] = ListingForm()
    return render(request, 'create_listing.html', resp)


def log_out(request):
    auth = authenticate(request)
    #Ensure the user is logged in to access the page
    if not auth.get('logged_in'):
        return render(request, 'home_page.html',
                      {'message': {'status_message': "You're not logged in!"}})
    auth = request.COOKIES.get('auth_id')
    try:
        login_request = urllib.request.Request(url=EXP_API + 'user/logout/'+auth+'/', method='POST')
        logout_json = urllib.request.urlopen(login_request).read().decode('utf-8')
        logout_resp = json.loads(logout_json)
    except urllib.error.HTTPError:
        return render(request, 'home_page.html', {'message': {'status_message': 'Something went wrong when processing your request'}})
    # if the logout was successful, get the authenticator and set the cookie to it.
    if logout_resp['status'] == 'success':
        response = HttpResponseRedirect(reverse('home'))
        response.delete_cookie('auth_id')
        return response
        # Otherwise, send the errors in the message (including a status message)
    else:
        if 'status_message' not in logout_resp['errors']:
            logout_resp['errors']['status_message'] = 'Logout failed!'
        return render(request, 'home_page.html', {'message': logout_resp['errors']})


def home(request):
    resp = {}
    auth = authenticate(request)
    if auth['logged_in']:
        resp['logged_in'] = auth['username']
    try:
        top_req = urllib.request.Request(EXP_API + 'items/get_by/item_type/Top/')
        top_resp_json = urllib.request.urlopen(top_req).read().decode('utf-8')
        top_list = json.loads(top_resp_json)
    except urllib.error.HTTPError:
        top_list = {'data':[]}
    resp['tops'] = top_list
    try:
        btm_req = urllib.request.Request(EXP_API + 'items/get_by/item_type/Bottom/')
        btm_resp_json = urllib.request.urlopen(btm_req).read().decode('utf-8')
        btm_list = json.loads(btm_resp_json)
    except urllib.error.HTTPError:
        btm_list = {'data':[]}
    resp['bottoms'] = btm_list
    try:
        shoe_req = urllib.request.Request(EXP_API + 'items/get_by/item_type/Footwear/')
        shoe_resp_json = urllib.request.urlopen(shoe_req).read().decode('utf-8')
        shoe_list = json.loads(shoe_resp_json)
    except urllib.error.HTTPError:
        shoe_list = {'data':[]}
    resp['shoes'] = shoe_list
    return render(request, 'home_page.html', resp)


def display_item(request, item_id=0):
    try:
        req = urllib.request.Request(EXP_API + 'item/get_info/' + str(item_id) + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
    except urllib.error.HTTPError:
        return render(request, 'home_page.html', {'message':{'status_message':'Something went wrong when processing your request!'}})
    auth = authenticate(request)
    if auth['logged_in']:
        resp['logged_in'] = auth['username']
    return render(request, 'item_page.html', resp)


def authenticate(request):
    auth = request.COOKIES.get('auth_id')
    # If there's not a cookie, no way you're logged in.
    if not auth:
        return {'logged_in': False}
    try:
        req = urllib.request.Request(url=EXP_API + '/auth/' + auth + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
    except urllib.error.HTTPError:
        resp = {'logged_in': False}
    return resp
