import os
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from happypatent.users.models import User
from .utils import get_upload_path, file_validate


@python_2_unicode_compatible
class FileAttachment(models.Model):
    """
    - This Model can be attached to any models with any amount you like.
    - Models that would be attached to should have a GenericRelation field.
    - To get the model object attached by this FileAttachment can be done by content_object attribute.
    """
    file = models.FileField(upload_to=get_upload_path, validators=[file_validate])
    filename = models.CharField(_("File's Name"), max_length=100, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(_('Created Time'), auto_now_add=True, null=True)
    created_by = models.ForeignKey(verbose_name=_("Created by"),
                                   to=User,
                                   on_delete=models.SET_NULL,
                                   null=True)

    def get_absolute_url(self):
        return reverse("files:files-detail", args=[self.pk,])

    @property
    def file_url(self):
        return self.file.url

    @property
    def file_path(self):
        return self.file.path

    def related_object_name(self):
        return str(self.content_object)

    def __str__(self):
        if self.filename:
            return self.filename
        return "Attaching %s to %s" % (self.file_path, self.related_object_name())
