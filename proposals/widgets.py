from django.urls import reverse_lazy
from django.forms import Select, SelectMultiple


class AjaxSelect2Mixin(object):
    def __init__(self, data_view, attrs={}, choices=(), create_new=False, create_new_url=""):
        attrs["class"] = "form-control ajax-select2"
        attrs["style"] = "width: 100%"
        attrs["data-url"] = reverse_lazy(data_view)
        if create_new:
            attrs["able-create-new"] = "true"
            attrs["create-new-url"] = reverse_lazy(create_new_url)
        else:
            attrs["able-create-new"] = "false"
        super(AjaxSelect2Mixin, self).__init__(attrs, choices)


class AjaxSelect2Widget(AjaxSelect2Mixin, Select):
    pass


class AjaxSelect2MultipleWidget(AjaxSelect2Mixin, SelectMultiple):
    pass


class MySelect2Widget(Select):
    def __init__(self, attrs={}, choices=()):
        attrs["class"] = "form-control select2-js"
        attrs["style"] = "width: 100%"
        super(MySelect2Widget, self).__init__(attrs, choices)

    class Media:
        js = ["js/render-select2.js"]


