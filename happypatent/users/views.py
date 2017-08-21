from django.core.urlresolvers import reverse
from django.views.generic import DetailView, RedirectView, UpdateView, TemplateView, View
from django.shortcuts import redirect, render_to_response
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from django.db import transaction
from datetime import datetime
from .models import User, CalendarEvent
from .forms import UserProfileModelForm
from proposals.models import Patent, Agent, ControlEvent, Proposal, Inventor
from billboard.models import Post, Comment
from django.utils.timezone import utc
from dateutil.relativedelta import relativedelta

DATE_FMT = "%a, %d %b %Y %X GMT"


@transaction.non_atomic_requests
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = 'username'
    # get parameter in url
    slug_url_kwarg = 'username'


@transaction.non_atomic_requests
class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileModelForm
    template_name = "users/user_form.html"

    def get_success_url(self):

        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


@transaction.non_atomic_requests
def home(request):
    if request.user.is_authenticated:
        return redirect("users:dashboard")
    else:
        return render_to_response("pages/home.html", context={})


@transaction.non_atomic_requests
class DashBoardView(LoginRequiredMixin, TemplateView):
    template_name = "users/dashboard.html"

    def get_context_data(self, **kwargs):
        kwargs = super(DashBoardView, self).get_context_data(**kwargs)
        # Warning modal: Get patents that are almost due.
        kwargs["expire_events"] = ControlEvent.objects.filter(
            Q(created_by=self.request.user) &
            Q(complete_date__isnull=True) &
            Q(deadline__lte=timezone.now() + relativedelta(days=7))
        ).order_by('+deadline')
        return kwargs


@transaction.non_atomic_requests
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

        # Get control event objects, which deadline or control date is within start and end date.
        qs = ControlEvent.objects.filter(
            Q(created_by__username=username) &
            (Q(control_date__range=(start_date, end_date)) |
             Q(deadline__range=(start_date, end_date))) &
            Q(complete_date__isnull=True)
        )
        for q in qs:
            control_date = q.control_date.strftime("%Y-%m-%d")
            deadline = q.deadline.strftime("%Y-%m-%d")
            e = {
                "id": q.patent.pk,
                "case_id": q.patent.case_id,
                "url": q.patent.get_absolute_url(),
                "control_date": control_date,
                "deadline": deadline,
                "description": "<strong>Control Item</strong>: %s, <strong>Control Date</strong>: %s, "
                               "<strong>Deadline</strong>: %s" % (
                    q.control_item_template(), control_date, deadline
                ),
            }
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


def getClassName(obj):
    """
    Use for timeline display icon.
    You should also add corresponding icon tag at js (var timeline_icon)
    """
    if isinstance(obj, Patent):
        return "patent"
    elif isinstance(obj, Agent):
        return "agent"
    elif isinstance(obj, Comment):
        return "comment"
    elif isinstance(obj, Post):
        return "post"
    elif isinstance(obj, Proposal):
        return "proposal"
    elif isinstance(obj, Inventor):
        return "inventor"
    return None


@transaction.non_atomic_requests
class TimeLineAjaxView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponse(status=400)
        user = request.user
        start = request.GET.get("start", None)
        end = request.GET.get("end", None)
        activities = user.actor_actions.all()
        if start:
            start = datetime.fromtimestamp(float(start), tz=utc)
            activities = activities.filter(timestamp__lt=start)
        if end:
            end = datetime.fromtimestamp(float(end), tz=utc)
            activities = activities.filter(timestamp__gt=end)
        if start or not end:
            activities = activities[:10]
        response = []
        for activity in activities:
            e = {
                "timesince": activity.timesince(),
                "timestamp": activity.timestamp.strftime(DATE_FMT),
                "actor": str(activity.actor),
                "actor_url": activity.actor.get_absolute_url(),
                "verb": activity.verb,
                "object": str(activity.action_object),
                "object_url": str(activity.action_object.get_absolute_url()),
                "object_type": getClassName(activity.action_object)
            }
            response.append(e)
        return JsonResponse(response, safe=False)
