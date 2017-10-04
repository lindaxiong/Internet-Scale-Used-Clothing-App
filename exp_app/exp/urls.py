from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^items/(?P<item_id>[0-9a-z]+)/$', views.get_item_page_info, name='item-page-info'),
    url(r'^items/', views.get_top_items, name='top-results')
]
