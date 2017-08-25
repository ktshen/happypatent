from django.template import loader
from django.template import Context
from tika import unpack
from haystack import indexes
from .models import FileAttachment


class FileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    filename = indexes.CharField(model_attr='filename')
    related_object_name = indexes.CharField(model_attr="content_object")
    created = indexes.DateTimeField(model_attr='created')
    created_by = indexes.CharField(model_attr="created_by", null=True)
    remarks = indexes.CharField(model_attr="remarks")

    def get_model(self):
        return FileAttachment

    def prepare(self, obj):
        data = super(FileIndex, self).prepare(obj)
        extracted_data = self.extract_file_contents(obj.file_path)
        t = loader.select_template(('search/indexes/fileattachments/fileattachment_text.txt',))
        data['text'] = t.render(Context({'object': obj,
                                         'metadata': extracted_data["metadata"],
                                         'content': extracted_data["content"]}))
        return data

    @staticmethod
    def extract_file_contents(file_path):
        return unpack.from_file(file_path)

    def prepare_related_object(self, obj):
        return str(obj)

    def prepare_created_by(self, obj):
        if obj.created_by:
            return "%s %s" % (obj.created_by.get_username(), obj.created_by.get_full_name())
        else:
            return ""
