from django.urls import path
from django.views.generic.base import View
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'  # Define the application name space. This allows to organize URLS by application and use the name when referring to them

urlpatterns = [
    # Post view
    path(route='', view=views.post_list, name='post_list'),
    # path(route='', view=views.PostListView.as_view(), name='post_list'),
    path(route='<int:year>/<int:month>/<int:day>/<slug:post>',
         view=views.post_detail, name='post_detail'),
    path(route='<int:post_id>/share/', view=views.post_share, name='post_share'),
    path(route='tag/<slug:tag_slug>/',
         view=views.post_list, name='post_list_by_tag'),
    path(route='feed/', view=LatestPostsFeed(), name='post_feed')
]
