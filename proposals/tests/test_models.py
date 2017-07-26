from test_plus import TestCase
from django.core.exceptions import ValidationError
from ..models import Patent, Client, Agent


class PatentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.make_user(cls)
        cls.test_data = {"case_id": "17P000",
                         "chinese_title": "測試文件",
                         "english_title": "testing patent",
                         "country": 'US',
                         "priority": 'no',
                         "created_by": cls.user}
        cls.patent = Patent.objects.create(**cls.test_data)

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


class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.make_user(cls)
        cls.test_data = {
            'abbr_client': "test_abbr",
            'client_ch_name': "測試",
            'client_en_name': "test-client",
            'country': "country",
            'post_address': "test",
            'phone_number': "0123456789",
            'repr_chinese_name': "測試代表人",
            'repr_english_name': "test_repr",
            'primary_owner': "test-owner",
            'created_by': cls.user
        }
        cls.client_model = Client.objects.create(**cls.test_data)

    def test_field_must_required(self):
        self.assertFalse(self.client_model._meta.get_field('abbr_client').blank)
        self.assertFalse(self.client_model._meta.get_field('client_ch_name').blank)
        self.assertFalse(self.client_model._meta.get_field('client_en_name').blank)
        self.assertFalse(self.client_model._meta.get_field('country').blank)
        self.assertFalse(self.client_model._meta.get_field('post_address').blank)
        self.assertFalse(self.client_model._meta.get_field('phone_number').blank)
        self.assertFalse(self.client_model._meta.get_field('repr_chinese_name').blank)
        self.assertFalse(self.client_model._meta.get_field('repr_english_name').blank)
        try:
            self.client_model.full_clean()
        except ValidationError as e:
            self.fail("Client full_clean() method raise a ValidationError: %s" % e)

    def test__str__(self):
        self.assertEqual(str(self.client_model), self.test_data["client_ch_name"])

    def test_client_name(self):
        self.assertEqual(self.client_model.name, self.client_model.client_ch_name)

    def test_get_absolute_url(self):
        self.assertEqual(self.client_model.get_absolute_url(), "/proposals/client/1/detail/")

    def test_client_pk(self):
        self.assertEqual(self.client_model.pk, self.client_model.client_id)


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

