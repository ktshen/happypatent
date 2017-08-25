from django.shortcuts import render
from .models import FileAttachment


class FileAttachmentViewMixin(object):
    """ Create a FileAttachment for model """
    def form_valid(self, form):
        response = super(FileAttachmentViewMixin, self).form_valid(form)
        for file in self.request.FILES.getlist('file'):
            attachment = FileAttachment(file=file, content_object=self.object)
            attachment.created_by = self.request.user
            attachment.save()
        return response
