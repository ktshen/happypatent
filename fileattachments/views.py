import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from happypatent.base.views import BaseDeleteView, BaseDataTableAjaxMixin
from .models import FileAttachment


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


class FileDetailView(LoginRequiredMixin, DetailView):
    model = FileAttachment
    template_name = "fileattachments/file_detail.html"


class FileListView(LoginRequiredMixin, BaseDataTableAjaxMixin, ListView):
    model = FileAttachment
    template_name = "fileattachments/file_list.html"
    table_fields = ["filename", "related_object_name", "created", "created_by"]


class FileDeleteView(LoginRequiredMixin, BaseDeleteView):
    model = FileAttachment
    success_url = reverse_lazy("files:files-list")
    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        fp = self.object.file_path
        self.object.delete()
        if os.path.isfile(fp):
            os.remove(fp)
        if self.request.is_ajax():
            return JsonResponse(data=[], status=200, safe=False)
        else:
            return HttpResponseRedirect(self.get_success_url())
