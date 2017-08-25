# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^detail/(?P<pk>[-\w]+)/$', views.FileDetailView.as_view(), name='files-detail'),
    url(r'^list/$', views.FileListView.as_view(), name='files-list'),
    url(r'^delete/$', views.FileDeleteView.as_view(), name='files-delete')
]
