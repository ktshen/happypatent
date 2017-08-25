from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from happypatent.users.models import User


@python_2_unicode_compatible
class BaseModel(models.Model):
    remarks = models.TextField(_('Remarks'), blank=True)

    created_by = models.ForeignKey(verbose_name=_("Created by"),
                                   to=User,
                                   on_delete=models.SET_NULL,
                                   null=True)

    created = models.DateTimeField(_('Created Time'),
                                   auto_now_add=True)

    update = models.DateTimeField(_('Latest Update'),
                                  auto_now=True,
                                  null=True)

    class Meta:
        abstract = True
