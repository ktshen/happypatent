import factory
from ..models import Patent, ControlEvent
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class PatentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patent

    english_title = "testing patent %d"
    country = 'US'
    priority = 'no'

    @factory.sequence
    def case_id(n):
        return "17P{0:03}".format(n)

    @factory.sequence
    def chinese_title(n):
        return "測試文件-%d" % n

    @factory.sequence
    def english_title(n):
        return "testing_patent-%d" % n


class ControlEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ControlEvent

    control_item = "1"
    control_date = timezone.now()
    deadline = timezone.now() + relativedelta(days=10)

