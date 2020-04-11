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
