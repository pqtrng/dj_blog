from django.urls import path
from django.views.generic.base import View
from . import views

app_name = 'blog'  # Define the application name space. This allows to organize URLS by application and use the name when referring to them

urlpatterns = [
    # Post view
    # path(route='', view=views.post_list, name='post_list'),
    path(route='', view=views.PostListView.as_view(), name='post_list'),
    path(route='<int:year>/<int:month>/<int:day>/<slug:post>',
         view=views.post_detail, name='post_detail')
]
