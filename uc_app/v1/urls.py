from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^home/', views.hompeage),
    url(r'^user/create', views.create_user),
    url(r'^user/get/[0-9]+', views.get_user),
    url(r'^user/edit/[0-9]+'), views.edit_user),
    url(r'^item/create', views.create_item),
    url(r'^item/get/[0-9]+', views.get_item),
    url(r'^item/edit/[0-9]+', views.edit_item)
]
