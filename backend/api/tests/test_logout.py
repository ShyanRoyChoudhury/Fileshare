from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('Logout')  # Ensure the URL name matches your urls.py

    def test_logout_success(self):
        """
        Test successful logout.
        """
        # Make a GET request to the Logout endpoint
        response = self.client.get(self.url)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'status': 'Success'
            }
        })

        # Verify the access_token cookie is deleted
        self.assertEqual(
            response.cookies.get('access_token').value, ''  # Cookie value is empty
        )
        self.assertEqual(
            response.cookies.get('access_token')['max-age'], 0  # Cookie is expired
        )

    def test_logout_cookie_attributes(self):
        """
        Test that the access_token cookie has the correct attributes.
        """
        # Make a GET request to the Logout endpoint
        response = self.client.get(self.url)

        # Verify the cookie attributes
        access_token_cookie = response.cookies.get('access_token')
        self.assertIsNotNone(access_token_cookie)  # Ensure the cookie exists
        self.assertEqual(access_token_cookie['samesite'], 'Lax')  # SameSite attribute
        self.assertEqual(access_token_cookie['path'], '/')  # Cookie path
        self.assertEqual(access_token_cookie['domain'], 'localhost')  # Cookie domain