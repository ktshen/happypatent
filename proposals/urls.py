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
    url(r'^agent/delete/$', views.AgentDeleteView.as_view(), name='agent-delete'),
    url(r'^agent/select2/$', views.AgentSelect2View.as_view(), name='agent-select2'),

    url(r'^client/create/$', views.ClientCreateView.as_view(), name='client-create'),
    url(r'^client/(?P<client_id>\d+)/detail/$', views.ClientDetailView.as_view(),
                                             name='client-detail'),
    url(r'^client/(?P<client_id>\d+)/update/$', views.ClientUpdateView.as_view(),
                                             name='client-update'),
    url(r'^client/list/$', views.ClientListView.as_view(), name='client-list'),
    url(r'^client/delete/$', views.ClientDeleteView.as_view(), name='client-delete'),
    url(r'^client/select2/$', views.ClientSelect2View.as_view(), name='client-select2'),

    # url(r'^employee/create/$', views.EmployeeCreateView.as_view(), name='employee-create'),
    # url(r'^employee/(?P<pk>\d+)/detail/$', views.EmployeeDetailView.as_view(),
    #     name='employee-detail'),
    # url(r'^employee/(?P<pk>\d+)/update/$', views.EmployeeUpdateView.as_view(),
    #     name='employee-update'),
    # url(r'^employee/list/$', views.EmployeeListView.as_view(), name='employee-list'),
    # url(r'^employee/delete/$', views.EmployeeDeleteView.as_view(), name='employee-delete'),

    url(r'^patent/create/$', views.PatentCreateView.as_view(), name='patent-create'),
    url(r'^patent/(?P<case_id>[-\w]+)/detail/$', views.PatentDetailView.as_view(),
        name='patent-detail'),
    url(r'^patent/(?P<case_id>[-\w]+)/update/$', views.PatentUpdateView.as_view(),
        name='patent-update'),
    url(r'^patent/list/$', views.PatentListView.as_view(), name='patent-list'),
    url(r'^patent/delete/$', views.PatentDeleteView.as_view(), name='patent-delete'),

    url(r'^inventor/create/$', views.InventorCreateView.as_view(), name='inventor-create'),
    url(r'^inventor/(?P<pk>[-\w]+)/detail/$', views.InventorDetailView.as_view(),
        name='inventor-detail'),
    url(r'^inventor/(?P<pk>[-\w]+)/update/$', views.InventorUpdateView.as_view(),
        name='inventor-update'),
    url(r'^inventor/list/$', views.InventorListView.as_view(), name='inventor-list'),
    url(r'^inventor/delete/$', views.InventorDeleteView.as_view(), name='inventor-delete'),
    url(r'^inventor/select2/$', views.InventorSelect2View.as_view(), name='inventor-select2'),

    url(r'^control-event/create/$', views.ControlEventCreateView.as_view(), name='control-event-create'),
    url(r'^control-event/(?P<pk>[-\w]+)/update/$', views.ControlEventUpdateView.as_view(),
        name='control-event-update'),
    url(r'^control-event/delete/$', views.ControlEventDeleteView.as_view(), name='control-event-delete'),

    url(r'^chinese_to_english/$', views.ChineseAddressToEnglishView.as_view(), name='chinese-english-address'),

]
