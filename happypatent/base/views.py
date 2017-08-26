from django.views.generic.edit import DeleteView
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic import ListView
from django.db.models import Model
from haystack.query import SearchQuerySet


class BaseDeleteView(DeleteView):
    """ Base View for deleting models."""

    http_method_names = [u'post']
    success_message = "%(field)s was deleted successfully."

    def post(self, request, *args, **kwargs):
        try:
            self.kwargs[self.slug_url_kwarg] = request.POST["slug_field"]
        except KeyError:
            return HttpResponseBadRequest()
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user == self.object.created_by:
            return HttpResponseBadRequest("You have no privilege to delete this item")
        success_url = self.get_success_url()
        self.object_name = str(self.object)
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_success_message(self, cleaned_data):
        if self.object_name:
            return self.success_message % dict(field=self.object_name)
        else:
            return "Delete Successfully."


class BaseDataTableAjaxMixin(ListView):
    """
    JQUERY DataTable's source
    The original idea is getting HTML through method GET and and collecting data source through method POST
    """
    table_fields = []
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        searching = False

        if not request.is_ajax():
            return HttpResponseBadRequest("AJAX ONLY.")
        if request.POST["search[value]"]:
            self.object_list = self.haystack_search(request.POST["search[value]"])
            searching = True
        else:
            self.object_list = self.model._default_manager.all().order_by(*self.ordering)
        paginator = self.get_paginator(self.object_list, self.paginate_by)
        page = paginator.page(self.get_page_num())
        data = self.get_data(page, searching)
        response = {
            'draw': request.POST['draw'],
            'recordsTotal': paginator.count,
            'recordsFiltered': paginator.count,
            'data': data
        }
        return JsonResponse(data=response, safe=False)

    def get_data(self, page, searching=False):
        data = []
        for item in page.object_list:
            if searching:
                # Haystack will return SearchResult class
                item = item.object
            row = []
            for field in self.table_fields:
                attr = getattr(item, field)
                if callable(attr) :
                    attr = str(attr())
                if not attr:
                    attr = "None"
                if isinstance(attr, Model):
                    attr = self.wrapped_with_url(str(attr), attr.get_absolute_url())
                else:
                    if not isinstance(attr, str):
                        attr = str(attr)
                    if field == self.table_fields[0]:
                        attr = self.wrapped_with_url(attr, item.get_absolute_url())
                row.append(attr)
            data.append(row)
        return data

    def get_page_num(self):
        return int(((int(self.request.POST["start"]))/self.paginate_by)+1)

    @staticmethod
    def wrapped_with_url(string, url):
        return '<a href="{0}">{1}</a>'.format(url, string)

    def haystack_search(self, query):
        return SearchQuerySet().models(self.model).auto_query(query).load_all()
