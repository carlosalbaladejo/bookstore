from django.test import TestCase
from django.urls import reverse

from .models import Book


class BookTests(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title='Moby-Dick',
            author='Herman Melville',
            price=25.00,
        )

    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Moby-Dick')
        self.assertEqual(f'{self.book.author}', 'Herman Melville')
        self.assertEqual(self.book.price, 25.00)

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Moby-Dick')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Moby-Dick')
        self.assertTemplateUsed(response, 'books/book_detail.html')
