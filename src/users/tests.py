"""
    users/tests.py
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from .forms import CustomUserCreationForm

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


class SignupTests(TestCase):

    username = 'newuser'
    email = 'newuser@email.com'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'Hi there! I should not be here!')

    def test_signup_form(self):
        User.objects.create_user(self.username, self.email)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(User.objects.all()[0].username, self.username)
        self.assertEqual(User.objects.all()[0].email, self.email)
