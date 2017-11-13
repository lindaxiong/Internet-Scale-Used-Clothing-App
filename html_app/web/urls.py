from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^item/display/(?P<item_id>[0-9a-z]+)/$', views.display_item, name='display-item'),
    url(r'^user/signup/$', views.sign_up, name='user-sign-up'),
    url(r'^$', views.home, name='home'),
    url(r'^user/login/$', views.log_in, name='log-in'),
    url(r'^user/logout/$', views.log_out, name='log-out'),
    url(r'^item/create/$', views.create_listing, name='create-listing'),
    url(r'^search/$', views.search_listings, name='search-listings'),
]
