from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.urls.base import reverse
from django.contrib.contenttypes.fields import GenericRelation

from ckeditor.fields import RichTextField
from proposals.models import FileAttachment
from happypatent.users.models import User


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(_('Title'), max_length=100)
    slug = models.SlugField(unique=True, blank=True, max_length=30)
    text = RichTextField()
    author = models.ForeignKey(verbose_name=_("Created by"),
                               to=User,
                               on_delete=models.SET_NULL,
                               null=True)
    files = GenericRelation(FileAttachment, related_query_name='post')
    created = models.DateTimeField(_('Created Time'),
                                   auto_now_add=True)

    update = models.DateTimeField(_('Latest Update'),
                                  auto_now=True,
                                  null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("billboard:detail", args=[self.slug,])

    def save(self, *args, **kwargs):
        s = "%s %d" % (self.title[:10], int(timezone.now().timestamp()))
        self.slug = slugify(s, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Comment(models.Model):
    text = models.TextField(max_length=150)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(to=User,
                                   on_delete=models.SET_NULL,
                                   null=True)
    created = models.DateTimeField(_('Created Time'),
                                   auto_now_add=True)

    def __str__(self):
        return self.text[:10]

    def get_absolute_url(self):
        return reverse("billboard:detail", args=[self.post.slug,])+"#comment"
