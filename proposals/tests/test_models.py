from test_plus import TestCase
from django.core.exceptions import ValidationError
from ..models import Agent, Inventor, ControlEvent
from .factories import PatentFactory, ControlEventFactory


class PatentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.make_user(cls)
        cls.patent = PatentFactory(created_by=cls.user)

    def test_fields_must_required(self):
        self.assertFalse(self.patent._meta.get_field("case_id").blank)
        self.assertFalse(self.patent._meta.get_field("chinese_title").blank)
        self.assertFalse(self.patent._meta.get_field("english_title").blank)
        self.assertFalse(self.patent._meta.get_field("country").blank)
        self.assertFalse(self.patent._meta.get_field("case_id").blank)
        try:
            self.patent.full_clean()
        except ValidationError as e:
            self.fail("Patent full_clean() method raise a ValidationError: %s" % e)

    def test_get_absolute_url(self):
        self.assertEqual(self.patent.get_absolute_url(), "/proposals/patent/%s/detail/" % self.patent.case_id)

    def test__str__(self):
        self.assertEqual(str(self.patent), self.patent.case_id)

    def test_unique_case_id(self):
        self.assertTrue(self.patent._meta.get_field("case_id").unique)


class AgentTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.make_user(cls)
        cls.test_data = {
            'agent_title': "test-agent-title",
            'country': "USA",
            'created_by': cls.user
        }
        cls.agent = Agent.objects.create(**cls.test_data)

    def test_field_must_required(self):
        self.assertFalse(self.agent._meta.get_field('agent_title').blank)
        self.assertFalse(self.agent._meta.get_field('country').blank)
        try:
            self.agent.full_clean()
        except ValidationError as e:
            self.fail("Client full_clean() method raise a ValidationError: %s" % e)

    def test__str__(self):
        self.assertEqual(str(self.agent), self.test_data["agent_title"])

    def test_agent_pk(self):
        self.assertEqual(self.agent.pk, self.agent.agent_id)

    def test_get_absolute_url(self):
        self.assertEqual(self.agent.get_absolute_url(), "/proposals/agent/1/detail/")


class InventorTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.make_user(cls)
        c = ClientFactory(created_by=cls.user)
        cls.test_data = {
            'chinese_name': "測試資料",
            'english_name': "test-1",
            'country': "country",
            'post_address': "Road-1",
            'english_address': "Road-2",
            'client': c,
            'created_by': cls.user
        }
        cls.model = Inventor.objects.create(**cls.test_data)

    def test_field_must_required(self):
        self.assertFalse(self.model._meta.get_field('chinese_name').blank)
        self.assertFalse(self.model._meta.get_field('english_name').blank)
        self.assertFalse(self.model._meta.get_field('country').blank)
        self.assertFalse(self.model._meta.get_field('post_address').blank)
        self.assertFalse(self.model._meta.get_field('english_address').blank)
        try:
            self.model.full_clean()
        except ValidationError as e:
            self.fail("Inventor's full_clean() method raise a ValidationError: %s" % e)

    def test__str__(self):
        self.assertEqual(str(self.model), self.test_data["chinese_name"])

    def test_get_absolute_url(self):
        self.assertEqual(self.model.get_absolute_url(), "/proposals/inventor/1/detail/")


class ControlEventTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = cls.make_user(cls)
        patent = PatentFactory(created_by=cls.user)
        cls.model = ControlEventFactory(patent=patent, created_by=cls.user)

    def test_field_must_required(self):
        self.assertFalse(self.model._meta.get_field('control_item').blank)
        self.assertFalse(self.model._meta.get_field('control_date').blank)
        self.assertFalse(self.model._meta.get_field('deadline').blank)
        self.assertFalse(self.model._meta.get_field('patent').blank)
        try:
            self.model.full_clean()
        except ValidationError as e:
            self.fail("Control Event's full_clean() method raise a ValidationError: %s" % e)

    def test__str__(self):
        self.assertEqual(str(self.model), "ControlEvent_17P000_File new application")

    def test_control_item_verbal(self):
        self.assertEqual(str(dict(ControlEvent.CONTROL_ITEM_CHOICES)[self.model.control_item]),
                         "File new application")
