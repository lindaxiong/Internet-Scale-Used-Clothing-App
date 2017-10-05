from django.shortcuts import render
from django.http import JsonResponse
import urllib.request
import urllib.parse
import json

MODEL_API = 'http://models-api:8000/api/v1/'

# this is for error checking:
# initially, this was just a list. now i put it in a dictionary
# put all data as the value of key 'data': response = {'data': {keys: values we have in our model_api
def get_top_items(request, item_ids=(4,5,6)):
    response = {'data': []}
    for item_id in item_ids:
        item_req = urllib.request.Request(MODEL_API + 'item/get/' + str(item_id) + '/')
        item_resp_json = urllib.request.urlopen(item_req).read().decode('utf-8')
        item_resp = json.loads(item_resp_json)
        user_id = item_resp['seller']
        user_req = urllib.request.Request(MODEL_API + 'user/get/' + str(user_id) + '/')
        user_resp_json = urllib.request.urlopen(user_req).read().decode('utf-8')
        user_resp = json.loads(user_resp_json)
        result_resp = {'item_name':item_resp['item_name'],
                        'item_price':item_resp['item_price'],
                        'seller_username':user_resp['username'],
                        'description':item_resp['description'],
                        'image_url':item_resp['image_url'],
                        'item_size':item_resp['item_size'],
                        'item_type':item_resp['item_type'],
                        'item_id':item_resp['id']}
        response['data'].append(result_resp)
    return JsonResponse(response, status=200)


def get_item_page_info(request, item_id=0):
    response = {'data': []}
    try:
        item_req = urllib.request.Request(MODEL_API + 'item/get/' + str(item_id) + '/')
        item_resp_json = urllib.request.urlopen(item_req).read().decode('utf-8')
        item_resp = json.loads(item_resp_json)
    except urllib.error.HTTPError:
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
