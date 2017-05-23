from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^dashboard/$',
        view=views.DashBoardView.as_view(),
        name='dashboard'
    ),
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    url(
        regex=r'user/^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),

    url(
        regex=r'^calendar_event/$',
        view=views.RetrieveCalendarEvent.as_view(),
        name='calendar_event'
    ),

    url(
        regex=r'^calendar_event/create/$',
        view=views.CalendarEventCreation.as_view(),
        name='calendar_event_create'
    ),
    url(
        regex=r'^calendar_event/update/$',
        view=views.CalendarEventUpdate.as_view(),
        name='calendar_event_update'
    ),
    url(
        regex=r'^calendar_event/delete/$',
        view=views.CalendarEventRemoval.as_view(),
        name='calendar_event_delete'
    ),
    url(
        regex=r'^$',
        view=views.home,
        name='home'
    ),
]
