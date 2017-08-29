# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

# ckeditor urls is defined in base urls.py

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/detail/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^create/$', views.PostCreateView.as_view(), name='create'),
    url(r'^list/$', views.PostListView.as_view(), name='list'),
    url(r'^(?P<slug>[-\w]+)/update/$', views.PostUpdateView.as_view(), name='update'),
    url(r'^remove/$', views.post_remove, name='remove'),
    url(r'^detail/(?P<slug>[-\w]+)/comment/$', views.CommentCreateView.as_view(), name='comment'),
    url(r'^file_upload/$', views.BillBoardFileUploadView.as_view(), name='file_upload'),
]
