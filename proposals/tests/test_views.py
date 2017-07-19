from test_plus.test import TestCase
from ..models import Patent, FileAttachment
import os
from ..utils import get_upload_path


def generate_file():
    f = open("test.txt", "w")
    for i in range(10 ** 5):
        f.write(str(i))
    f.close()

class PatentCreateViewTest(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.client.force_login(user=self.user)
        self.test_data = {"case_id": "17P000",
                          "chinese_title": "測試文件",
                          "english_title": "testing patent",
                          "country": 'US',
                          "priority": 'no',
                          "patent_term": "2017-07-01",
                          "extended_days": "30"}

    def test_login_required(self):
        self.client.logout()
        self.assertLoginRequired("proposals:patent-create")

    def test_can_send_POST_request(self):
        response = self.post(self.reverse("proposals:patent-create"), data=self.test_data)
        new_item = Patent.objects.first()
        self.assertRedirects(response, self.reverse("proposals:patent-detail", new_item.case_id))
        self.assertEqual(new_item.case_id, self.test_data["case_id"] + "-" + self.test_data["country"])
        self.assertEqual(new_item.chinese_title, self.test_data["chinese_title"])
        self.assertEqual(new_item.english_title, self.test_data["english_title"])
        self.assertEqual(new_item.country, self.test_data["country"])
        self.assertEqual(new_item.created_by, self.user)

    def test_can_send_GET_request(self):
        response = self.get(self.reverse("proposals:patent-create"))
        self.response_200(response)

    def test_other_country_without_case_id(self):
        Patent.objects.create(**self.test_data, created_by=self.user)
        response = self.get(self.reverse("proposals:patent-create"), data={"other_country": "true"})
        self.response_400(response)
        response = self.get(self.reverse("proposals:patent-create"), data={
            "other_country": "true",
            "case_id": self.test_data["case_id"]
        })
        self.response_200(response)

    def test_check_final_patent_term_for_US(self):
        self.post(self.reverse("proposals:patent-create"), data=self.test_data)
        new_item = Patent.objects.first()
        self.assertEqual(new_item.final_patent_term.strftime(format="%Y-%m-%d"), "2017-07-31")

    def test_file_attachment(self):
        generate_file()
        with open('test.txt') as fp:
            self.test_data["file"] = fp
            self.post(self.reverse("proposals:patent-create"), data=self.test_data)
        try:
            file = FileAttachment.objects.first()
            self.assertTrue("test" in file.filename)
            self.assertEqual(os.path.dirname(str(file.file)), os.path.dirname(get_upload_path(None, "test.txt")))
        finally:
            os.remove("test.txt")
            os.remove(file.file.path)
