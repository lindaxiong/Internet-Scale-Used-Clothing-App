from django.conf.urls import url
from . import views

# simplified the get_item_page_info url to just items/<item_id>, added
# get_many_items functino to return multiple items for the spalsh screen (currently that's hard-coded
# because i just load the 3 items from fixtures)
urlpatterns = [
    url(r'^items/(?P<item_id>[0-9a-z]+)/$', views.get_item_page_info, name='item-page-info'),
    url(r'^items/', views.get_top_items, name='top-results')
]
