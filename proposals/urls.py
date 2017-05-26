# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^agent/create/$', views.AgentCreateView.as_view(), name='agent-create'),
    url(r'^agent/(?P<agent_id>\d+)/detail/$', views.AgentDetailView.as_view(),
                                        name='agent-detail'),
    url(r'^agent/(?P<agent_id>\d+)/update/$', views.AgentUpdateView.as_view(),
                                        name='agent-update'),
    url(r'^agent/list/$', views.AgentListView.as_view(), name='agent-list'),

    url(r'^client/create/$', views.ClientCreateView.as_view(), name='client-create'),
    url(r'^client/(?P<client_id>\d+)/detail/$', views.ClientDetailView.as_view(),
                                             name='client-detail'),
    url(r'^client/(?P<client_id>\d+)/update/$', views.ClientUpdateView.as_view(),
                                             name='client-update'),
    url(r'^client/list/$', views.ClientListView.as_view(), name='client-list'),

    url(r'^employee/create/$', views.EmployeeCreateView.as_view(), name='employee-create'),
    url(r'^employee/(?P<pk>\d+)/detail/$', views.EmployeeDetailView.as_view(),
        name='employee-detail'),
    url(r'^(?P<pk>\d+)/update/$', views.EmployeeUpdateView.as_view(),
        name='employee-update'),
    url(r'^employee/list/$', views.EmployeeListView.as_view(), name='employee-list'),

    url(r'^patent/create/$', views.PatentCreateView.as_view(), name='patent-create'),
    url(r'^patent/(?P<case_id>[-\w]+)/detail/$', views.PatentDetailView.as_view(),
        name='patent-detail'),
    url(r'^patent/(?P<case_id>[-\w]+)/update/$', views.PatentUpdateView.as_view(),
        name='patent-update'),
    url(r'^patent/list/$', views.PatentListView.as_view(), name='patent-list'),

    url(r'^contact_person/create/$', views.ContactPersonCreateView.as_view(), name='contact_person-create'),
    url(r'^contact_person/(?P<pk>\d+)/detail/$', views.ContactPersonDetailView.as_view(), name='contact_person-detail'),
    url(r'^contact_person/(?P<pk>\d+)/update/$', views.ContactPersonUpdateView.as_view(), name='contact_person-update'),
    url(r'^contact_person/list/$', views.ContactPersonListView.as_view(), name='contact_person-list'),

    url(r"^fields/auto.json$", views.Select2View.as_view(), name="select2-json"),
]
