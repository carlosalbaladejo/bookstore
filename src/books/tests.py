from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from .models import Book, Review


class BookTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='reviewuser',
            email='review@email.com',
            password='testpass123',
        )
        self.permission = Permission.objects.get(codename='special_status')
        self.book = Book.objects.create(
            title='Moby-Dick', author='Herman Melville', price=25.00,
        )
        self.review = Review.objects.create(
            book=self.book, review='Great Book', author=self.user,
        )

    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Moby-Dick')
        self.assertEqual(f'{self.book.author}', 'Herman Melville')
        self.assertEqual(self.book.price, 25.00)

    def test_book_list_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/books/' % (reverse('account_login'))
        )
        response = self.client.get(
            '%s?next=/books/' % (reverse('account_login'))
        )
        self.assertContains(response, 'Log In')

    def test_book_list_view_for_logged_user(self):
        self.client.login(email='review@email.com', password='testpass123')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Moby-Dick')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_view_w_permissions(self):
        self.client.login(email='review@email.com', password='testpass123')
        self.user.user_permissions.add(self.permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Moby-Dick')
        self.assertContains(response, 'Great Book')
        self.assertTemplateUsed(response, 'books/book_detail.html')
