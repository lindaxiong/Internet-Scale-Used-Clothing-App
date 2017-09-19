from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^home/', views.hompeage),
    url(r'^user/create', views.create_user),
    url(r'^user/[0-9]+', views.access_user),
    url(r'^item/create', views.create_item),
    url(r'^item/[0-9]+', views.access_item),
]
