from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr="title")
    content = indexes.CharField(model_attr="text")
    author = indexes.CharField(model_attr='author', null=True)
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return Post

    def prepare_author(self, obj):
        if obj.author:
            return "%s %s" % (obj.author.get_username(), obj.author.get_full_name())
        else:
            return ""
