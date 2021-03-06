from django.db.models.signals import post_save
from actstream import action
from .models import Patent, Agent, Proposal, Inventor


def patent_handler(sender, instance, created, **kwargs):
    creator = instance.created_by
    if created:
        action.send(creator, verb='creates', action_object=instance)
    else:
        action.send(creator, verb='updates', action_object=instance)


def agent_handler(sender, instance, created, **kwargs):
    creator = instance.created_by
    if created:
        action.send(creator, verb='creates', action_object=instance)
    else:
        action.send(creator, verb='updates', action_object=instance)


def proposal_handler(sender, instance, created, **kwargs):
    creator = instance.created_by
    if created:
        action.send(creator, verb='creates', action_object=instance)
    else:
        action.send(creator, verb='updates', action_object=instance)


def inventor_handler(sender, instance, created, **kwargs):
    creator = instance.created_by
    if created:
        action.send(creator, verb='creates', action_object=instance)
    else:
        action.send(creator, verb='updates', action_object=instance)

post_save.connect(patent_handler, sender=Patent)
post_save.connect(agent_handler, sender=Agent)
post_save.connect(proposal_handler, sender=Proposal)
post_save.connect(inventor_handler, sender=Inventor)

