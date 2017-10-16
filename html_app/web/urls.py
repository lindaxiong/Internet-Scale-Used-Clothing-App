from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^item/display/(?P<item_id>[0-9a-z]+)/$', views.display_item, name='display-item'),
    url(r'^user/signup/$', views.sign_up, name='user-sign-up'),
    url(r'^$', views.home, name='home')
]
