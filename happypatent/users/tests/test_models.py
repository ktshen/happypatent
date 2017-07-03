from test_plus.test import TestCase
from .factories import UserFactory
from  proposals.models import Patent
from ..models import CalendarEvent
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class TestUser(TestCase):
    user_factory = UserFactory

    def setUp(self):
        self.user = self.make_user()
        self.patent = Patent.objects.create(**{
            "case_id": "17P000",
            "chinese_title": "測試案件",
            "english_title": "test_case",
            "country": "TW",
            "created_by": self.user
        })

    def test__str__(self):
        self.assertEqual(
            self.user.__str__(),
            'testuser'  # This is the default username for self.make_user()
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.user.get_absolute_url(),
            '/user/testuser/'
        )

    def test_gender_template(self):
        self.assertEqual(
            self.user.gender_template(),
            "Male"
        )
        self.user.gender = ""
        self.assertEqual(
            self.user.gender_template(),
            ""
        )

    def test_get_user_patents(self):
        self.assertEqual(
            self.user.get_user_patents()[0],
            self.patent
        )


class TestCalendarEvent(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.calendar_event = CalendarEvent.objects.create(
            title="testevent",
            start_date=timezone.now(),
            end_date=timezone.now() + relativedelta(months=1,days=1),
            background_color="#FF3333",
            border_color="#FF3333",
            created_by=self.user
        )

    def test__str__(self):
        self.assertEqual(
            self.calendar_event.__str__(),
            'testevent'
        )
