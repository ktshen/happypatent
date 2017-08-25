from uuid import uuid4
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError


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
