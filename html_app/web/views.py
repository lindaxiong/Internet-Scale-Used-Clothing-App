from django.shortcuts import render
import urllib.request
import urllib.parse
import json

EXP_API = 'http://exp-api:8000/api/v1/'


def home(request):
    req = urllib.request.Request(EXP_API + 'items/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return render(request, 'home_page.html', resp)


def display_item(request, item_id=0):
    req = urllib.request.Request(EXP_API + 'items/' + str(item_id) + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return render(request, 'item_page.html', resp)
