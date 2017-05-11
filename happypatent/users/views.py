from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, TemplateView
from django.shortcuts import redirect, render_to_response
from django.http.response import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User


def home(request):
    if request.user.is_authenticated:
        return redirect("users:dashboard")
    else:
        return render_to_response("pages/home.html", context={})


class DashBoardView(LoginRequiredMixin, TemplateView):
    template_name = "users/dashboard.html"


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


