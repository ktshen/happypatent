from django.conf import settings
from django.core.exceptions import ValidationError


def image_validate(value):
    if value.size > settings.IMAGE_SIZE_LIMITATION:
        raise ValidationError('File too large. Size should not exceed 5 MiB.')
    img_ext = value.name.split('.')
    if len(img_ext) > 2:
        raise ValidationError('File\'s name should not contain more than 2 \'.\' (dots).')
    img_ext = img_ext[1].lower()
    allowed = settings.IMAGE_ALLOWED_EXTENSION
    if img_ext not in allowed:
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
