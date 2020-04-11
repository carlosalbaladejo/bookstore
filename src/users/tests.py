"""
    users/tests.py
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from .forms import CustomUserCreationForm

from .views import SignUpPageView


User = get_user_model()

USERNAME = 'test'
EMAIL = 'test@test.com'
PASSWORD = 'testpass'


class CustomUserTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username=USERNAME, email=EMAIL, password=PASSWORD,
        )
        self.assertEqual(user.username, USERNAME)
        self.assertEqual(user.email, EMAIL)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username='super' + USERNAME,
            email='super' + EMAIL,
            password=PASSWORD,
        )
        self.assertEqual(admin_user.username, 'super' + USERNAME)
        self.assertEqual(admin_user.email, 'super' + EMAIL)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SignUpPageTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'Hi There, I should not be here!')

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(
            view.func.__name__,
            SignUpPageView.as_view().__name__
        )
