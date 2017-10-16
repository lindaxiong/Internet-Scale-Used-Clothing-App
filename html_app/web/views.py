from django.shortcuts import render
import urllib.request
import urllib.parse
from web.forms import UserCreationForm
import json
import random

EXP_API = 'http://exp-api:8000/api/v1/'

def sign_up(request):
    if request.method == "POST":
        #doesn't return any error codes, don't need to try/catch 
        create_usr_req = urllib.request.Request(url=EXP_API + 'user/create/', method='POST', data=request.body)
        create_usr_json = urllib.request.urlopen(create_usr_req).read().decode('utf-8')
        cu_resp = json.loads(create_usr_json)
        form = UserCreationForm()
        if cu_resp['status'] == 'success':
            return render(request, 'signup.html', {'form':form, 'message':{'status_message':'User successfully created!'}})
        else:
            cu_resp['errors']['status_message'] = 'User creation failed!'
            return render(request, 'signup.html', {'form':form, 'message':cu_resp['errors']})
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form':form})


# FIX to do less overall work than right now - maybe change functionality?
def home(request):
    resp = {}
    top_req = urllib.request.Request(EXP_API + 'items/get_by/item_type/Top/')
    top_resp_json = urllib.request.urlopen(top_req).read().decode('utf-8')
    top_resp = json.loads(top_resp_json)
    top_list = []
    if len(top_resp) > 3:
        for i in range(3):
            index = random.randint(0, len(top_resp)-1)
            top_list.append(top_resp[index])
            top_resp.remove(top_resp[index])
    else:
        top_list = top_resp
    resp['tops'] = top_list
    btm_req = urllib.request.Request(EXP_API + 'items/get_by/item_type/Bottom/')
    btm_resp_json = urllib.request.urlopen(btm_req).read().decode('utf-8')
    btm_resp = json.loads(btm_resp_json)
    btm_list = []
    if len(btm_resp) > 3:
        for i in range(3):
            index = random.randint(0, len(btm_resp)-1)
            btm_list.append(btm_resp[index])
            btm_resp.remove(btm_resp[index])
    else:
        btm_list = btm_resp
    resp['bottoms'] = btm_list
    shoe_req = urllib.request.Request(EXP_API + 'items/get_by/item_type/Footwear/')
    shoe_resp_json = urllib.request.urlopen(shoe_req).read().decode('utf-8')
    shoe_resp = json.loads(shoe_resp_json)
    shoe_list = []
    if len(shoe_resp) > 3:
        for i in range(3):
            index = random.randint(0, len(shoe_resp)-1)
            shoe_list.append(shoe_resp[index])
            shoe_resp.remove(shoe_resp[index])
    else:
        shoe_list = shoe_resp
    resp['shoes'] = shoe_list
    return render(request, 'home_page.html', resp)


def display_item(request, item_id=0):
    req = urllib.request.Request(EXP_API + 'items/' + str(item_id) + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return render(request, 'item_page.html', resp)
