from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect

from django_select2.views import AutoResponseView

from .models import Employee, Patent, Agent, Client, ContactPerson, User
from .forms import EmployeeModelForm, PatentModelForm, ContactPersonModelForm, ClientModelForm, AgentModelForm


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
        form.save()
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


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    template_name = "proposals/employee_create.html"
    form_class = EmployeeModelForm


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        context["object_fields_data"] = get_model_fields_data(self.object)
        return context


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee


class PatentCreateView(LoginRequiredMixin, UserAppendCreateViewMixin, CreateView):
    model = Patent
    template_name = 'proposals/patent_create_form.html'
    form_class = PatentModelForm

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


class PatentDetailView(LoginRequiredMixin, DetailView):
    model = Patent


class PatentUpdateView(LoginRequiredMixin, UpdateView):
    model = Patent


class ContactPersonCreateView(LoginRequiredMixin, UserAppendCreateViewMixin,
                              AjaxableResponseMixin, CreateView):
    model = ContactPerson
    template_name = "proposals/contact_person_create.html"
    form_class = ContactPersonModelForm


class ContactPersonDetailView(LoginRequiredMixin, DetailView):
    model = ContactPerson
    template_name = "contact_person_detail.html"


class ContactPersonUpdateView(LoginRequiredMixin, UpdateView):
    model = ContactPerson


class AgentCreateView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    model = Agent
    template_name = "proposals/agent_create.html"
    form_class = AgentModelForm


class AgentDetailView(LoginRequiredMixin, DetailView):
    model = Agent
    slug_field = "agent_id"
    slug_url_kwarg = "agent_id"


class AgentUpdateView(LoginRequiredMixin, UpdateView):
    model = Agent


class ClientCreateView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    model = Client
    template_name = "proposals/client_create.html"
    form_class = ClientModelForm


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    slug_field = "client_id"
    slug_url_kwarg = "client_id"


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client


