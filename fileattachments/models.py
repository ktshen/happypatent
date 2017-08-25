import os
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from happypatent.base.models import BaseModel
from .utils import get_upload_path


class FileAttachment(BaseModel):
    """
    - This Model can be attached to any models with any amount you like.
    - Models that would be attached to should have a GenericRelation field.
    - To get the model object attached by this FileAttachment can be done by content_object attribute.
    """
    file = models.FileField(upload_to=get_upload_path)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(_('Created Time'), auto_now_add=True, null=True)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def get_absolute_url(self):
        pass

    @property
    def file_url(self):
        return self.file.url

    @property
    def file_path(self):
        return self.file.path

    def related_object_name(self):
        return str(self.content_object)

    def __str__(self):
        return "Attaching %s to %s" % (self.filename, str(self.content_object))
