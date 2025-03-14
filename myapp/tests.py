from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse

class HomePageTest(TestCase):
    def test_homepage_message(self):
        response = self.client.get(reverse('homepage'))  # Use the URL name
        self.assertEqual(response.status_code, 200)  # Check if page loads
        self.assertContains(response, "Welcome to the Homepage!")  # Check message
