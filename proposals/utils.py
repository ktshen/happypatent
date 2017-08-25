from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import ValidationError
from uuid import uuid4

from proposals import models


class CaseIDGenerator(object):
    """
    - Class that helps model 'Patent' to process latest case id, which could get or set a latest
      case id from and to the cache.
    - Case ID Format: <year> P <case no.>.  Example: '17P010', '18P1101'
    """
    def __init__(self):
        self.cache_key = "latest_patent_case_id"

    @property
    def current_year(self):
        return timezone.now().strftime("%Y")[-2:]

    def get_latest_id(self):
        # latest_id = cache.get(self.cache_key)
        # if latest_id is None:
        #     latest_id = self.search_latest_id()
        # else:
        #     if self.current_year != latest_id[:2]:
        #         latest_id = self.search_latest_id()
        return self.search_latest_id()

    def update_latest_id(self, case_id):
        if case_id != cache.get(self.cache_key):
            return self.search_latest_id()
        year, num = case_id.split("P")
        if year != self.current_year:
            return False
        latest_id = self.build_case_id(year, int(num)+1)
        cache.set(self.cache_key, latest_id, None)

    @staticmethod
    def build_case_id(year, num):
        if type(num) is int:
            num = str(num)
            # length of num should be longer or equal to 3
            if len(num) < 3:
                num = '0' * (3 - len(num)) + num
        if type(year) is int:
            year = str(year)
        if len(year) == 4:
            year = year[-2:]
        return year + "P" + num

    def search_latest_id(self):
        qs = models.Patent.objects.filter(case_id__startswith=self.current_year)
        max_num = 0
        for p in qs:
            s = int(p.case_id.split("P")[1].split("-")[0]) + 1
            if s > max_num:
                max_num = s
        latest_id = self.build_case_id(self.current_year, max_num)
        cache.set(self.cache_key, latest_id, None)
        return latest_id


def get_upload_path(instance, filename):
    return 'files/%s/%s/%s' % (timezone.now().strftime("%Y-%m-%d"), uuid4().hex[:6], filename)


def file_validate(value):
    if value.size > settings.FILE_SIZE_LIMITATION:
        raise ValidationError('File too large. Size should not exceed %d MiB.' %
                              int(settings.FILE_SIZE_LIMITATION/10**6))
    file_ext = value.name.split('.')
    if len(file_ext) > 2:
        raise ValidationError('File\'s name should not contain more than 2 \'.\' (dots).')
    file_ext = file_ext[1].lower()
    allowed = settings.FILE_ALLOWED_EXTENSION
    if file_ext not in allowed:
        msg = 'File\'s extension should be'
        for i in range(len(allowed)):
            if i == 0:
                msg = msg + " " + allowed[i]
            elif i == len(allowed)-1:
                msg = msg + " or " + allowed[i]
            else:
                msg = msg + ", " + allowed[i]
        msg = msg + '.'
        raise ValidationError(msg)

YES_OR_NO = (
        ('yes', 'Yes'),
        ('no', 'No')
    )


