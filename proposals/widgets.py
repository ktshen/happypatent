from django.urls import reverse_lazy
from django.forms import Select


class AjaxSelect2Widget(Select):
    def __init__(self, data_view, attrs={}, choices=(), multiple=False, create_new=False, create_new_url=""):
        attrs["class"] = "form-control ajax-select2"
        attrs["style"] = "width: 100%"
        attrs["data-url"] = reverse_lazy(data_view)
        attrs["able-create-new"] = create_new
        attrs["create-new-url"] = create_new_url
        if multiple:
            attrs["multiple"] = True
        super(AjaxSelect2Widget, self).__init__(attrs, choices)

    class Media:
        js = ["js/ajax-select2.js"]


class MySelect2Widget(Select):
    def __init__(self, attrs={}, choices=()):
        attrs["class"] = "form-control select2-js"
        attrs["style"] = "width: 100%"
        super(MySelect2Widget, self).__init__(attrs, choices)

    class Media:
        js = ["js/render-select2.js"]


