from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.list import BaseListView
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.contrib import messages
from django.db.models import Q
from dateutil.relativedelta import relativedelta
import geocoder

from .models import Employee, Patent, Agent, Client, User, FileAttachment, \
                    Inventor, ControlEvent
from .forms import EmployeeModelForm, PatentModelForm, ClientModelForm, \
                   AgentModelForm, InventorModelForm, ControlEventModelForm
from .utils import CaseIDGenerator


def get_model_fields_data(obj):
    return [(field.name, getattr(obj,field.name)) for field in obj._meta.fields]


class _DeleteView(LoginRequiredMixin, DeleteView):
    http_method_names = [u'post']
    success_message = "%(field)s was deleted successfully."

    def post(self, request, *args, **kwargs):
        try:
            self.kwargs[self.slug_url_kwarg] = request.POST["slug_field"]
        except KeyError:
            return HttpResponseBadRequest()
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user == self.object.created_by:
            return HttpResponseBadRequest("You have no privilege to delete this item")
        success_url = self.get_success_url()
        self.object_name = str(self.object)
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_success_message(self, cleaned_data):
        if self.object_name:
            return self.success_message % dict(field=self.object_name)
        else:
            return "Delete Successfully."


class AjaxSelect2View(LoginRequiredMixin, BaseListView):
    search_fields = []
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        try:
            q = request.GET["q"]
        except KeyError:
            return HttpResponseBadRequest("No q in GET.")
        qs = [Q(**{i:q}) for i in self.search_fields]
        filter_query = qs.pop()
        for t in qs:
            filter_query |= t
        if not self.model:
            raise ImproperlyConfigured("Model parameter is missing. Please define it.")
        self.object_list = self.get_queryset(filter_query=filter_query)
        allow_empty = self.get_allow_empty()
        context = self.get_context_data(object_list=self.object_list)
        results = []
        if len(self.object_list):
            results = [
                {
                    'id': obj.pk,
                    'text': str(obj),
                }
                for obj in self.object_list
            ]
        elif "able_create_new" in request.GET and request.GET["able_create_new"] == "true":
            results.append({
                    'id': -1,
                    'text': "Create %s" % q
                })
        return JsonResponse({
            'items': results,
            'page': context['page_obj'].number
        }, safe=False)

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(kwargs["filter_query"])


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object = None
            context = self.get_context_data()
            s = render_to_string("proposals/ajax_modal.html",
                                 context={"form": context["form"]},
                                 request=request)
            return JsonResponse({"html": s})
        else:
            return super(AjaxableResponseMixin, self).get(request, *args, **kwargs)

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
        if not self.object:
            self.object = form.save(commit=False)
        self.object.created_by = User.objects.get(username=self.request.user.username)
        self.object.save()
        response = super(UserAppendCreateViewMixin, self).form_valid(form)
        return response


class FileAttachmentViewMixin(object):
    def form_valid(self, form):
        response = super(FileAttachmentViewMixin, self).form_valid(form)
        for file in self.request.FILES.getlist('file'):
            instance = FileAttachment(file=file, content_object=self.object)
            instance.save()
        return response


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


class EmployeeDeleteView(_DeleteView):
    model = Employee
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    success_url = reverse_lazy("proposals:employee-list")


class PatentMixin(object):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.patent_term and self.object.extended_days and self.object.country == "US":
            self.object.final_patent_term = self.object.patent_term + relativedelta(days=self.object.extended_days)
        return super(PatentMixin, self).form_valid(form)


class PatentCreateView(LoginRequiredMixin, SuccessMessageMixin, PatentMixin, UserAppendCreateViewMixin,
                       FileAttachmentViewMixin, CreateView):
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
                "inventor": patent.inventor.all()
            }
            if patent.client:
                init["client"] = patent.client
        else:
            init = {"case_id": CaseIDGenerator().get_latest_id()}
        return init

    def get_context_data(self, **kwargs):
        context = super(PatentCreateView, self).get_context_data(**kwargs)
        context["files"] = FileAttachment.objects.filter()
        return context

    def get(self, request, *args, **kwargs):
        if "other_country" in request.GET and request.GET["other_country"] == "true":
            self.other_country = True
            try:
                self.case_id = request.GET["case_id"]
            except KeyError:
                return HttpResponseBadRequest("Please specify case id.")
        else:
            self.other_country = False
        return super(PatentCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.other_country = None
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


class PatentUpdateView(LoginRequiredMixin, PatentMixin, FileAttachmentViewMixin, UpdateView):
    model = Patent
    slug_field = "case_id"
    slug_url_kwarg = "case_id"
    form_class = PatentModelForm
    template_name = "proposals/patent_create.html"


class PatentListView(LoginRequiredMixin, ListView):
    model = Patent
    ordering = ['-update', '-created']


class PatentDeleteView(_DeleteView):
    model = Patent
    slug_field = "case_id"
    slug_url_kwarg = "case_id"
    success_url = reverse_lazy("proposals:patent-list")


class ControlEventEditMixin(object):
    def get_initial(self):
        if hasattr(self, "patent"):
            return {"case_id": self.patent.case_id}
        else:
            return {}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.patent = get_object_or_404(Patent, case_id=form.cleaned_data["case_id"])
        return super(ControlEventEditMixin, self).form_valid(form)

    def get_success_url(self):
        if self.object.patent:
            return self.object.patent.get_absolute_url()
        else:
            return super(ControlEventEditMixin, self).get_success_url()


class ControlEventCreateView(LoginRequiredMixin, UserAppendCreateViewMixin, SuccessMessageMixin,
                             ControlEventEditMixin, CreateView):
    model = ControlEvent
    template_name = "proposals/control_event_create.html"
    form_class = ControlEventModelForm

    def get(self, request, *args, **kwargs):
        if "case_id" not in request.GET:
            return HttpResponseBadRequest("There's no case_id in request.")
        else:
            self.patent = get_object_or_404(Patent, case_id=request.GET["case_id"])
        if self.patent.control_event.count() >= 3:
            messages.add_message(request, messages.WARNING, 'The maximum amount of control event for each patent is 3.')
            return redirect(self.patent.get_absolute_url())
        return super(ControlEventCreateView, self).get(request, *args, **kwargs)


class ControlEventUpdateView(LoginRequiredMixin, SuccessMessageMixin, ControlEventEditMixin, UpdateView):
    model = ControlEvent
    form_class = ControlEventModelForm
    template_name = "proposals/control_event_create.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.patent = self.object.patent
        return super(ControlEventUpdateView, self).get(request, *args, **kwargs)


class ControlEventDeleteView(_DeleteView):
    model = ControlEvent
    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    def get_success_url(self):
        return self.object.patent.get_absolute_url()


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


class AgentUpdateView(LoginRequiredMixin, UpdateView):
    model = Agent
    slug_field = "agent_id"
    slug_url_kwarg = "agent_id"
    template_name = "proposals/agent_create.html"
    form_class = AgentModelForm


class AgentListView(LoginRequiredMixin, ListView):
    model = Agent
    queryset = Agent.objects.all().order_by("country", "-created")


class AgentDeleteView(_DeleteView):
    model = Agent
    slug_field = 'agent_id'
    slug_url_kwarg = 'agent_id'
    success_url = reverse_lazy("proposals:agent-list")


class AgentSelect2View(AjaxSelect2View):
    model = Agent
    search_fields = ["agent_title__icontains"]


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

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context["inventor_list"] = Inventor.objects.filter(client=self.object).order_by("country")
        return context


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    slug_field = "client_id"
    slug_url_kwarg = "client_id"
    template_name = "proposals/client_create.html"
    form_class = ClientModelForm


class ClientListView(LoginRequiredMixin, ListView):
    model = Client


class ClientDeleteView(_DeleteView):
    model = Client
    slug_field = "client_id"
    slug_url_kwarg = "client_id"
    success_url = reverse_lazy("proposals:client-list")


class ClientSelect2View(AjaxSelect2View):
    model = Client
    search_fields = ["client_en_name__icontains", "client_ch_name__icontains"]


class InventorEditMixin(object):
    def get_initial(self):
        if self.request.method == "GET":
            if "client_id" in self.request.GET:
                client_id = self.request.GET["client_id"]
                client = Client.objects.get(client_id=client_id)
                return {"client_id": client.client_id,
                        "post_address": client.post_address,
                        "english_address": client.english_address}
            elif self.object and hasattr(self.object, "client"):
                client_id = self.object.client.client_id
                return {"client_id": client_id}
            else:
                return HttpResponseBadRequest("Can't find client_id.")
        else:
            return self.initial.copy()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = get_object_or_404(Client, client_id=form.cleaned_data["client_id"])
        return super(InventorEditMixin, self).form_valid(form)


class InventorCreateView(LoginRequiredMixin, UserAppendCreateViewMixin, SuccessMessageMixin,
                         InventorEditMixin, CreateView):
    model = Inventor
    template_name = "proposals/inventor_create.html"
    form_class = InventorModelForm
    success_message = "%(chinese_name)s was created successfully."

    def get(self, request, *args, **kwargs):
        if not "client_id" in request.GET:
            return HttpResponseBadRequest("No Client specified to create new inventor.")
        return super(InventorCreateView, self).get(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            chinese_name=self.object.chinese_name,
        )


class InventorDetailView(LoginRequiredMixin, DetailView):
    model = Inventor


class InventorUpdateView(LoginRequiredMixin, InventorEditMixin, UpdateView):
    model = Inventor
    template_name = "proposals/inventor_create.html"
    form_class = InventorModelForm


class InventorListView(LoginRequiredMixin, ListView):
    model = Inventor


class InventorDeleteView(_DeleteView):
    model = Inventor
    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    def get_success_url(self):
        return self.object.client.get_absolute_url()


class InventorSelect2View(AjaxSelect2View):
    model = Inventor
    search_fields = ["chinese_name__istartswith", "english_name__istartswith"]

    def get_queryset(self, *args, **kwargs):
        if not self.request.GET["client_id"]:
            return HttpResponseBadRequest("Need client_id to get the corresponding inventors.")
        return self.model.objects.filter(client__client_id=self.request.GET["client_id"])\
                                 .filter(kwargs["filter_query"])


class ChineseAddressToEnglishView(View):
    http_method_names = [u'get']

    def get(self, request, *args, **kwargs):
        address = self.request.GET.get("address", "")
        error = ""
        result = ""
        if address:
            google_r = geocoder.google(address)
            if not google_r.address or not google_r.ok:
                error = "It is not a valid address."
            else:
                result = self.chinese_to_english(address, google_r.address)
        else:
            error = "Address field is empty."
        if error:
            return JsonResponse({"error": error})
        return JsonResponse({"english_address": result})

    def chinese_to_english(self, address, r):
        if "No." in r and "號" not in address:
            a = r.split("No. ")
            b = a[1].split(", ", 1)[1]
            r = a[0] + b
        if "樓" in address:
            floor = self.find_number(address, address.index("樓"), -1)
            if "樓之" in address and floor:
                dash_floor = self.find_number(address, address.index("樓之") + 1, +1)
                if dash_floor:
                    r = floor + "F-" + dash_floor + ", " + r
            elif floor:
                r = floor + "F" + ", " + r
        if "室" in address:
            room = self.find_number(address, address.index("室"), -1)
            if room:
                r = "Rm. " + room + ", " + r
        return r

    @staticmethod
    def find_number(address, index, no):
        # find forward: no = -1
        # find backward: no = +1
        number = "1234567890"
        s = ""
        index += no
        while len(address) > index >= 0:
            if address[index] in number:
                if no == -1:
                    s = address[index] + s
                else:
                    s = s + address[index]
            else:
                break
            index += no
        return s
