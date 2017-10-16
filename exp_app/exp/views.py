from django.shortcuts import render
from django.http import JsonResponse
import urllib.request
import urllib.parse
import json

MODEL_API = 'http://models-api:8000/api/v1/'

def create_user(request):
    try:
        create_usr_req = urllib.request.Request(url=MODEL_API + 'user/create/', method='POST', data=request.body)
        #Passes the request sent to this method into the Model layer - .body is encoded rather than .POST
        create_usr_json = urllib.request.urlopen(create_usr_req).read().decode('utf-8')
        cu_resp = json.loads(create_usr_json)
        result_resp = {}
        #if the returned dicitonary has "errors", something failed 
        if 'errors' in cu_resp.keys():
            result_resp = {'status':'failed',
            'errors':cu_resp['errors']}
        else:
            result_resp = {'status':'success',
            'userID':cu_resp['userID']}
        return JsonResponse(result_resp, status=200)
    except urllib.error.HTTPError:
        #Should only error out if get is submitted instead of POST.
        return JsonResponse({'status':'failed', 'errors':{'status_message':'invalid request type'}}, status=200)

def get_filtered_items(request, field, criteria):
    response = {'data': []}
    items = []
    try:
        item_req = urllib.request.Request(MODEL_API + 'item/get-by/' + field + '/' + criteria + '/')
        item_resp_json = urllib.request.urlopen(item_req).read().decode('utf-8')
        item_resp = json.loads(item_resp_json)
        items = item_resp
    except urllib.error.HTTPError:
        #returns empty response if item can't be recovered.
        return JsonResponse(response)
    for item in items:
        print(item)
        user_id = item['fields']['seller']
        username = ''
        #username is only supplied if it can be found.
        try:
            user_req = urllib.request.Request(MODEL_API + 'user/get/' + str(user_id) + '/')
            user_resp_json = urllib.request.urlopen(user_req).read().decode('utf-8')
            user_resp = json.loads(user_resp_json)
            username = user_resp['username']
        except urllib.error.HTTPError:
            username = ''
        result_resp = {'item_name':item['fields']['item_name'],
                        'item_price':item['fields']['item_price'],
                        'seller_username':username,
                        'description':item['fields']['description'],
                        'image_url':item['fields']['image_url'],
                        'item_size':item['fields']['item_size'],
                        'item_type':item['fields']['item_type'],
                        'item_id':item['pk']}
        response['data'].append(result_resp)
    return JsonResponse(response, status=200)


def get_item_page_info(request, item_id=0):
    response = {'data': []}
    try:
        item_req = urllib.request.Request(MODEL_API + 'item/get/' + str(item_id) + '/')
        item_resp_json = urllib.request.urlopen(item_req).read().decode('utf-8')
        item_resp = json.loads(item_resp_json)
    except urllib.error.HTTPError:
        #auto-returns if it can't find the associated item
        response['data'].append({'item_name':"Item Not Found"})
        return JsonResponse(response)
    try:
        user_id = item_resp['seller']
        user_req = urllib.request.Request(MODEL_API + 'user/get/' + str(user_id) + '/')
        user_resp_json = urllib.request.urlopen(user_req).read().decode('utf-8')
        user_resp = json.loads(user_resp_json)
        username = user_resp['username']
    except urllib.error.HTTPError:
        username = ''
    response['data'].append({'item_name':item_resp['item_name'],
    'item_price':item_resp['item_price'],
    'seller_username':username,
    'description':item_resp['description'],
    'image_url':item_resp['image_url'],
    'item_size':item_resp['item_size'],
    'item_type':item_resp['item_type']})
    return JsonResponse(response, status=200)


# Create your views here.
