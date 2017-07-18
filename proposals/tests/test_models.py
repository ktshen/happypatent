from test_plus import TestCase
from django.core.exceptions import ValidationError
from ..models import Patent


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
