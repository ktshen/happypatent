from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, TemplateView, View
from django.shortcuts import redirect, render_to_response
from django.http.response import HttpResponse, Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from datetime import datetime
from .models import User, CalendarEvent
from proposals.models import Patent
import pytz

DATE_FMT = "%a, %d %b %Y %X GMT"


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = 'username'
    # get parameter in url
    slug_url_kwarg = 'username'

    def get(self, request, *args, **kwargs):
        if self.request.user.username != self.kwargs.get(self.slug_url_kwarg):
            raise Http404("You have no privilege to search other user's profile.")
        else:
            super(UserDetailView, self).get(self, request, *args, **kwargs)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['first_name', 'last_name','id_number', 'gender',
              'county', 'address', 'home_number', 'mobile_number',
              'office_number', 'spouse_name', 'education','experience',
              'comment', 'profile_pic']

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


def home(request):
    if request.user.is_authenticated:
        return redirect("users:dashboard")
    else:
        return render_to_response("pages/home.html", context={})


class DashBoardView(LoginRequiredMixin, TemplateView):
    template_name = "users/dashboard.html"


class RetrieveCalendarEvent(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponse(status=400)
        return super(RetrieveCalendarEvent, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        username = self.request.user.username
        start_date = datetime.utcfromtimestamp(float(request.GET['start'])).date()
        end_date = datetime.utcfromtimestamp(float(request.GET['end'])).date()
        events = []

        # Get patent objects, which deadline or control date is within start and end date.
        qs = Patent.objects.filter(
            Q(created_by__username=username) &
            (Q(control_date__range=(start_date, end_date)) | Q(deadline__range=(start_date, end_date)))
        )
        for q in qs:
            e = {
                "id": q.pk,
                "case_id": q.case_id,
                "url": q.get_absolute_url(),
            }
            if q.control_date >= start_date and q.control_date <= end_date:
                e["control_date"] = q.control_date.strftime("%Y-%m-%d")
            if q.deadline >= start_date and q.deadline <= end_date:
                e["deadline"] = q.deadline.strftime("%Y-%m-%d")
            events.append(e)

        # Get User's Calendar event
        qs = CalendarEvent.objects.filter(
            Q(created_by__username=username) &
            (Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date)))
        )
        for q in qs:
            e = {
                "id": q.pk,
                "title": q.title,
                "backgroundColor": q.background_color,
                "border-color": q.border_color,
                "start": q.start_date.strftime("%Y-%m-%d"),
            }
            if q.end_date:
                e["end"] = q.end_date.strftime("%Y-%m-%d")
            events.append(e)
        return JsonResponse(events, safe=False)


class CalendarEventCreation(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponse(status=400)
        # Check required fields
        required_fields = ["title", "start", "backgroundColor", "border-color"]
        for f in required_fields:
            if f not in request.POST:
                return HttpResponse(status=400)
        try:
            new_event = CalendarEvent(
                title=request.POST["title"],
                start_date=datetime.strptime(request.POST["start"], DATE_FMT).date(),
                background_color=request.POST["backgroundColor"],
                border_color=request.POST["border-color"],
                created_by=User.objects.get(username=request.user.username)
            )
        except KeyError:
            return HttpResponse(status=400)
        new_event.save()
        return JsonResponse(data={"id": new_event.pk})


class CalendarEventUpdate(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponse(status=400)
        try:
            ev = CalendarEvent.objects.get(pk=request.POST["id"])
        except (KeyError, CalendarEvent.DoesNotExist):
            return HttpResponse("Event does not exist.", status=400)
        if "start" in request.POST.keys():
            ev.start_date = datetime.strptime(request.POST["start"], DATE_FMT).date()
        if "end" in request.POST.keys():
            ev.end_date = datetime.strptime(request.POST['end'], DATE_FMT).date()
        ev.save()
        return HttpResponse(status=200)


class CalendarEventRemoval(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponse(status=400)
        try:
            ev = CalendarEvent.objects.get(pk=request.POST["id"])
        except CalendarEvent.DoesNotExist:
            return HttpResponse("Event does not exist.", status=400)
        ev.delete(keep_parents=True)
        return HttpResponse(status=200)





