from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.messages.views import SuccessMessageMixin
from django_select2.views import AutoResponseView

from .models import Employee, Patent, Agent, Client, User
from .forms import EmployeeModelForm, PatentModelForm, ClientModelForm, AgentModelForm
from .utils import CaseIDGenerator

def get_model_fields_data(obj):
    return [(field.name, getattr(obj,field.name)) for field in obj._meta.fields]


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'id': self.object.pk,
                'text': str(self.object)
            }
            return JsonResponse(data)
        else:
            return response


class UserAppendCreateViewMixin(object):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = User.objects.get(username=self.request.user.username)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class Select2View(AutoResponseView):
    def get(self, request, *args, **kwargs):
        self.widget = self.get_widget_or_404()
        self.term = kwargs.get('term', request.GET.get('term', ''))
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        results = []
        if len(self.object_list):
            results = [
                {
                    'id': obj.pk,
                    'text': self.widget.label_from_instance(obj),
                }
                for obj in context['object_list']
            ]
        elif self.widget.able_ajax_create and self.term:
            results.append({
                    'id': -1,
                    'text': "Create %s" % self.term
                })
        return JsonResponse({
            'results': results,
            'more': context['page_obj'].has_next()
        })


class EmployeeCreateView(LoginRequiredMixin, UserAppendCreateViewMixin, SuccessMessageMixin, CreateView):
    model = Employee
    template_name = 'proposals/employee_form.html'
    form_class = EmployeeModelForm
    success_message = "%(field)s was created successfully"

    def get_success_message(self, cleaned_data):
        if self.object.chinese_name:
            field = self.object.chinese_name
        elif self.object.english_name:
            field = self.object.chinese_name
        else:
            field = self.object.employee_id
        return self.success_message % dict(field=field)


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = "proposals/employee_form.html"
    form_class = EmployeeModelForm


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee


class PatentCreateView(LoginRequiredMixin, UserAppendCreateViewMixin, SuccessMessageMixin, CreateView):
    model = Patent
    template_name = 'proposals/patent_create.html'
    form_class = PatentModelForm
    success_message = "%(case_id)s was created successfully"

    def get_initial(self):
        if self.other_country:
            patent = get_object_or_404(Patent, case_id=self.case_id)
            init = {
                "case_id": self.case_id.split("-")[0],
                "chinese_title": patent.chinese_title,
                "english_title": patent.english_title,
            }
        else:
            init = {"case_id": CaseIDGenerator().get_latest_id()}
        return init

    def get_context_data(self, **kwargs):
        context = super(PatentCreateView, self).get_context_data(**kwargs)
        context["modal_form"] = []
        widgets = self.get_form_class().Meta.widgets
        for f in widgets.keys():
            if getattr(widgets[f], "able_ajax_create", None):
                model_instance = widgets[f].modelform()
                model_instance.helper.form_id = widgets[f].attrs["modelform_id"]
                modelform_id = widgets[f].attrs["modelform_id"]
                context['modal_form'].append([
                    modelform_id,
                    model_instance,
                ])
        return context

    def get(self, request, *args, **kwargs):
        if "other_country" in request.GET and request.GET["other_country"] == "true":
            self.other_country = True
            try:
                self.case_id = request.GET["case_id"]
            except KeyError:
                return HttpResponseBadRequest()
        else:
            self.other_country = False
        return super(PatentCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        if "-" not in post["case_id"]:
            post["case_id"] = post["case_id"] + "-" + post["country"]
            self.request.POST = post
        return super(PatentCreateView, self).post(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            case_id=self.object.case_id,
        )


class PatentDetailView(LoginRequiredMixin, DetailView):
    model = Patent
    slug_field = "case_id"
    slug_url_kwarg = "case_id"


class PatentUpdateView(LoginRequiredMixin, UpdateView):
    model = Patent
    slug_field = "case_id"
    slug_url_kwarg = "case_id"
    form_class = PatentModelForm
    template_name = "proposals/patent_create.html"


class PatentListView(LoginRequiredMixin, ListView):
    model = Patent

    def get_queryset(self):
        return self.model.objects.filter(created_by__username=self.request.user.username).order_by('-update', '-created')


class AgentCreateView(LoginRequiredMixin, UserAppendCreateViewMixin, AjaxableResponseMixin,
                      SuccessMessageMixin, CreateView):
    model = Agent
    template_name = "proposals/agent_create.html"
    form_class = AgentModelForm
    success_message = "%(agent_title)s was created successfully."

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            agent_title=self.object.agent_title,
        )


class AgentDetailView(LoginRequiredMixin, DetailView):
    model = Agent
    slug_field = "agent_id"
    slug_url_kwarg = "agent_id"


class AgentListView(LoginRequiredMixin, ListView):
    model = Agent
    queryset = Agent.objects.all().order_by("country", "-created")


class AgentUpdateView(LoginRequiredMixin, UpdateView):
    model = Agent
    slug_field = "agent_id"
    slug_url_kwarg = "agent_id"
    template_name = "proposals/agent_create.html"
    form_class = AgentModelForm


class ClientCreateView(LoginRequiredMixin, UserAppendCreateViewMixin, AjaxableResponseMixin,
                       SuccessMessageMixin, CreateView):
    model = Client
    template_name = "proposals/client_create.html"
    form_class = ClientModelForm
    success_message = "%(client_ch_name)s was created successfully."

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            client_ch_name=self.object.client_ch_name,
        )


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    slug_field = "client_id"
    slug_url_kwarg = "client_id"


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    slug_field = "client_id"
    slug_url_kwarg = "client_id"
    template_name = "proposals/client_create.html"
    form_class = ClientModelForm


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
