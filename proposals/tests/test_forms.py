from django.conf import settings
from django.core.exceptions import ValidationError
from unittest.mock import Mock
from test_plus import TestCase
from ..utils import file_validate
from ..forms import PatentModelForm


class FileValidatorTest(TestCase):
    def setUp(self):
        self.file = Mock()

    def test_over_file_limitation(self):
        self.file.size = settings.FILE_SIZE_LIMITATION + 100000000
        with self.assertRaises(ValidationError):
            file_validate(self.file)

    def test_file_name_contain_double_dot(self):
        self.file.size = 10
        self.file.name = "test.yoyo.haha"
        with self.assertRaisesMessage(ValidationError,
                                      'File\'s name should not contain more than 2 \'.\' (dots).'):
            file_validate(self.file)

    def test_unavailable_file_extension(self):
        self.file.size = 10
        self.file.name = "test.yoyo"
        with self.assertRaises(ValidationError):
            file_validate(self.file)


class PatentModelFormTest(TestCase):
    def test_file_validators(self):
        form = PatentModelForm()
        self.assertEqual(form.fields["file"].validators[0], file_validate)
