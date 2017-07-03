from django.test import RequestFactory
from test_plus.test import TestCase
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from ..views import (
    UserRedirectView,
    UserUpdateView
)
from ..models import CalendarEvent


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()
        print("HI1")


class TestUserRedirectView(BaseUserTestCase):

    def test_get_redirect_url(self):
        # Instantiate the view directly. Never do this outside a test!
        view = UserRedirectView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        view.request = request
        # Expect: '/users/testuser/', as that is the default username for
        #   self.make_user()
        self.assertEqual(
            view.get_redirect_url(),
            '/user/testuser/'
        )


class TestUserUpdateView(BaseUserTestCase):

    def setUp(self):
        # call BaseUserTestCase.setUp()
        super(TestUserUpdateView, self).setUp()
        # Instantiate the view directly. Never do this outside a test!
        self.view = UserUpdateView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        self.view.request = request

    def test_get_success_url(self):
        # Expect: '/users/testuser/', as that is the default username for
        #   self.make_user()
        self.assertEqual(
            self.view.get_success_url(),
            '/user/testuser/'
        )

    def test_get_object(self):
        # Expect: self.user, as that is the request's user object
        self.assertEqual(
            self.view.get_object(),
            self.user
        )


class Testhome(BaseUserTestCase):
    def test_login(self):
        response = self.get("users:home")
        self.assertTemplateUsed(response, "pages/home.html")
        c = self.client.force_login(user=self.user)
        response = self.client.get(self.reverse("users:home"))
        self.assertRedirects(response=response, expected_url=self.reverse("users:dashboard"))


class TestCalendarEventMixin(object):
    def setUp(self):
        super(TestCalendarEventMixin, self).setUp()
        self.current_time = timezone.now()
        CalendarEvent.objects.create(
            title="testevent",
            start_date=self.current_time,
            end_date=self.current_time + relativedelta(months=1, days=1),
            background_color="#FF3333",
            border_color="#FF3333",
            created_by=self.user
        )
        CalendarEvent.objects.create(
            title="testevent-1",
            start_date=self.current_time,
            end_date=self.current_time + relativedelta(months=1, days=1),
            background_color="#FF3333",
            border_color="#FF3333",
            created_by=self.user
        )
        self.data = {
            "start"
        }


class TestRetrieveCalendarEvent(TestCalendarEventMixin, BaseUserTestCase):
    def test_get(self):
        pass



