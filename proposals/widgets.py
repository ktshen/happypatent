from random import randint

from django.core import signing
from django.urls import reverse
from django.forms import Select
from django.conf import settings
from django import forms

from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
from django_select2.cache import cache


class AjaxSelect2Mixin(object):
    """
    If Select2Widget is able to created through ajax, then the form must include attrs["modelform"] 
    and able_ajax_create = True in initialization
    """

    def __init__(self, attrs=None, choices=(), data_view="proposals:select2-json", able_ajax_create=False,
                 modelform=None, **kwargs):
        self.modelform = modelform
        self.able_ajax_create = able_ajax_create
        if self.modelform:
            if not attrs:
                attrs = {}
            attrs["style"] = "width: 100%"
            attrs["modelform_rand"] = str(randint(10000, 99999))
            attrs["modelform_id"] = signing.dumps(self.modelform.__name__+attrs["modelform_rand"]).rsplit(":", 1)[1]
        super(AjaxSelect2Mixin, self).__init__(attrs=attrs, choices=choices, data_view=data_view, **kwargs)

    def set_to_cache(self):
        # I overwrite this method in order to get able_ajax_create from cache
        queryset = self.get_queryset()
        cache.set(self._get_cache_key(), {
            'queryset':
                [
                    queryset.none(),
                    queryset.query,
                ],
            'cls': self.__class__,
            'search_fields': self.search_fields,
            'max_results': self.max_results,
            'url': self.get_url(),
            'dependent_fields': self.dependent_fields,
            'able_ajax_create': self.able_ajax_create,
        })

    class Media:
        js = ["js/jquery.form.min.js", "js/ajax-select2.js", ]



class AjaxSelect2Widget(AjaxSelect2Mixin, ModelSelect2Widget):
    pass


class AjaxSelect2MultipleWidget(AjaxSelect2Mixin, ModelSelect2MultipleWidget):
    pass


class MySelect2Widget(Select):
    def __init__(self, attrs=None, choices=()):
        if not attrs:
            attrs = {}
        attrs["class"] = "form-control select2-js"
        attrs["style"] = "width: 100%"
        super(MySelect2Widget, self).__init__(attrs, choices)

