# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # Agent
    url(r'^agent/create/$', views.AgentCreateView.as_view(), name='agent-create'),
    url(r'^agent/(?P<agent_id>\d+)/detail/$', views.AgentDetailView.as_view(),
                                        name='agent-detail'),
    url(r'^agent/(?P<agent_id>\d+)/update/$', views.AgentUpdateView.as_view(),
                                        name='agent-update'),
    url(r'^agent/list/$', views.AgentListView.as_view(), name='agent-list'),
    url(r'^agent/delete/$', views.AgentDeleteView.as_view(), name='agent-delete'),
    url(r'^agent/select2/$', views.AgentSelect2View.as_view(), name='agent-select2'),

    # Patent
    url(r'^patent/create/$', views.PatentCreateView.as_view(), name='patent-create'),
    url(r'^patent/(?P<case_id>[-\w]+)/detail/$', views.PatentDetailView.as_view(),
        name='patent-detail'),
    url(r'^patent/(?P<case_id>[-\w]+)/update/$', views.PatentUpdateView.as_view(),
        name='patent-update'),
    url(r'^patent/list/$', views.PatentListView.as_view(), name='patent-list'),
    url(r'^patent/delete/$', views.PatentDeleteView.as_view(), name='patent-delete'),

    # Proposal
    url(r'^proposal/create/$', views.ProposalCreateView.as_view(), name='proposal-create'),
    url(r'^proposal/(?P<pk>\d+)/detail/$', views.ProposalDetailView.as_view(),
        name='proposal-detail'),
    url(r'^proposal/(?P<pk>\d+)/update/$', views.ProposalUpdateView.as_view(),
        name='proposal-update'),
    url(r'^proposal/list/$', views.ProposalListView.as_view(), name='proposal-list'),
    url(r'^proposal/delete/$', views.ProposalDeleteView.as_view(), name='proposal-delete'),

    # Inventor
    url(r'^inventor/create/$', views.InventorCreateView.as_view(), name='inventor-create'),
    url(r'^inventor/(?P<pk>[-\w]+)/detail/$', views.InventorDetailView.as_view(),
        name='inventor-detail'),
    url(r'^inventor/(?P<pk>[-\w]+)/update/$', views.InventorUpdateView.as_view(),
        name='inventor-update'),
    url(r'^inventor/list/$', views.InventorListView.as_view(), name='inventor-list'),
    url(r'^inventor/delete/$', views.InventorDeleteView.as_view(), name='inventor-delete'),
    url(r'^inventor/select2/$', views.InventorSelect2View.as_view(), name='inventor-select2'),

    # Control Event
    url(r'^control-event/create/$', views.ControlEventCreateView.as_view(), name='control-event-create'),
    url(r'^control-event/(?P<pk>[-\w]+)/update/$', views.ControlEventUpdateView.as_view(),
        name='control-event-update'),
    url(r'^control-event/delete/$', views.ControlEventDeleteView.as_view(), name='control-event-delete'),

    url(r'^chinese_to_english/$', views.ChineseAddressToEnglishView.as_view(), name='chinese-english-address'),

    url(r'^file_upload/$', views.ProposalFileUploadView.as_view(), name='file_upload'),

]
