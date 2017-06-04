from django.contrib.staticfiles.templatetags.staticfiles import static
from .models import User

class UserProfileProcessor(object):
    def __init__(self, is_authenticated, username=None):
        self.is_authenticated = is_authenticated
        if is_authenticated:
            self.user = User.objects.get(username=username)
        else:
            self.user = None



def process(self, request):
    pass






