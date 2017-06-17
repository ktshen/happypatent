from django.db.models.signals import post_save
from actstream import action
from .models import Post, Comment


def post_handler(sender, instance, created, **kwargs):
    creator = instance.author
    if created:
        action.send(creator, verb='creates', action_object=instance)
    else:
        action.send(creator, verb='updates', action_object=instance)


def comment_handler(sender, instance, created, **kwargs):
    creator = instance.created_by
    if created:
        action.send(creator, verb='leaves a comment', action_object=instance)

post_save.connect(post_handler, sender=Post)
post_save.connect(comment_handler, sender=Comment)
