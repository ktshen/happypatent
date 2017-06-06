from django.db.models.signals import post_save
from actstream import action
from .models import Patent, Agent, Employee, Client, ContactPerson


def patent_handler(sender, instance, created, **kwargs):
    creator = instance.created_by
    if created:
        action.send(creator, verb='creates', action_object=instance)
    else:
        action.send(creator, verb='updates', action_object=instance)


def agent_handler(sender, instance, created, **kwargs):
    creator = instance.created_by
    print(creator)
    if created:
        action.send(creator, verb='creates', action_object=instance)
    else:
        action.send(creator, verb='updates', action_object=instance)


def employee_handler(sender, instance, created, **kwargs):
    creator = instance.created_by
    if created:
        action.send(creator, verb='creates', action_object=instance)
    else:
        action.send(creator, verb='updates', action_object=instance)


def client_handler(sender, instance, created, **kwargs):
    creator = instance.created_by
    if created:
        action.send(creator, verb='creates', action_object=instance)
    else:
        action.send(creator, verb='updates', action_object=instance)


def contact_person_handler(sender, instance, created, **kwargs):
    creator = instance.created_by
    if created:
        action.send(creator, verb='creates', action_object=instance)
    else:
        action.send(creator, verb='updates', action_object=instance)


post_save.connect(patent_handler, sender=Patent)
post_save.connect(agent_handler, sender=Agent)
post_save.connect(employee_handler, sender=Employee)
post_save.connect(client_handler, sender=Client)
post_save.connect(contact_person_handler, sender=ContactPerson)

