import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic import ListView, View
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from happypatent.base.views import BaseDeleteView, BaseDataTableAjaxMixin
from .models import FileAttachment
from .utils import file_validate


class FileAttachmentViewMixin(object):
    """ Create a FileAttachment for model """
    def form_valid(self, form):
        response = super(FileAttachmentViewMixin, self).form_valid(form)
        for file in self.request.FILES.getlist('file'):
            attachment = FileAttachment(file=file, content_object=self.object)
            attachment.filename = file.name
            attachment.created_by = self.request.user
            attachment.save()
        return response


class FileUploadView(LoginRequiredMixin, View):
    http_method_names = [u'post']
    model_list = {}
    delete_url = reverse_lazy('files:files-delete')

    def post(self, request, *args, **kwargs):
        POST = self.request.POST
        if "object_type" not in POST or "pk" not in POST:
            return HttpResponseBadRequest("No object_type or pk in request!")
        self.object = self.get_object(POST["object_type"], POST["pk"])
        file = self.request.FILES.getlist('files')
        if len(file) == 0:
            return HttpResponse(status=200, content="No files uploaded.")
        file = file[0]
        try:
            file_validate(file)
            attachment = FileAttachment(file=file, content_object=self.object)
            attachment.filename = file.name
            attachment.created_by = self.request.user
            attachment.save()
        except Exception as e:
            return JsonResponse(status=400, data={"message": str(e)})
        data = {
            "file_url": attachment.file_url,
            "file_pk": attachment.pk,
            "delete_url": self.delete_url
        }
        return JsonResponse(status=200, data=data, safe=False)

    def get_model_dict(self):
        self.model_dict = {}
        for model in self.model_list:
            self.model_dict[model._meta.verbose_name] = model

    def get_object(self, type, pk):
        self.get_model_dict()
        model = self.model_dict[type]
        return model.objects.get(pk=pk)


class FileDetailView(LoginRequiredMixin, DetailView):
    model = FileAttachment
    template_name = "fileattachments/file_detail.html"


class FileListView(LoginRequiredMixin, BaseDataTableAjaxMixin, ListView):
    model = FileAttachment
    template_name = "fileattachments/file_list.html"
    table_fields = ["filename", "related_object_name", "created", "created_by"]


class FileDeleteView(LoginRequiredMixin, View):
    success_url = reverse_lazy("files:files-list")
    http_method_names = [u'post']

    def post(self, request, *args, **kwargs):
        if 'pk' not in self.request.POST:
            return HttpResponseBadRequest("No pk.")
        pk = self.request.POST['pk']
        self.object = get_object_or_404(FileAttachment, pk=pk)
        fp = self.object.file_path
        self.object.delete()
        if os.path.isfile(fp):
            os.remove(fp)
        if self.request.is_ajax():
            return JsonResponse(data=[], status=200, safe=False)
        else:
            return HttpResponseRedirect(self.success_url)
