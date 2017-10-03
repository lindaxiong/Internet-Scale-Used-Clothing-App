from django.shortcuts import render
import urllib.request
import urllib.parse
import json

def display_item(request, item_id=0):
    req = urllib.request.Request('http://exp-api:8000/exp/v2/item/page/info/' + item_id + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return render(request, 'v3/item_page.html', resp)
# Create your views here.
