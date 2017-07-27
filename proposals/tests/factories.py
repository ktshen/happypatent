import factory
from ..models import Patent, Client, ControlEvent
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


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client
    abbr_client = "test_abbr"
    client_ch_name = "測試客戶"
    client_en_name = "test-client"
    country = "country"
    post_address = "test"
    phone_number = "0123456789"
    repr_chinese_name = "測試代表人"
    repr_english_name = "test_repr"
    primary_owner = "test-owner"


class ControlEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ControlEvent

    control_item = "1"
    control_date = timezone.now()
    deadline = timezone.now() + relativedelta(days=10)

