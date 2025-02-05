from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status

class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('signUp')  # Ensure the URL name matches your urls.py

    @patch('api.views.SignUpSerializer')
    def test_signup_success(self, MockSignUpSerializer):
        """
        Test successful user registration.
        """
        mock_serializer_instance = MockSignUpSerializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.signUp.return_value = {"created": True}

        response = self.client.post(
            self.url,
            {'idToken': 'valid_token', 'email': 'test@example.com'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['status'], 'Success')
        self.assertEqual(response.data['data']['message'], 'User Registered')

    @patch('api.views.SignUpSerializer')
    def test_signup_failure(self, MockSignUpSerializer):
        """
        Test user registration failure.
        """
        mock_serializer_instance = MockSignUpSerializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.signUp.return_value = {"created": False}

        response = self.client.post(
            self.url,
            {'idToken': 'valid_token', 'email': 'test@example.com'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['status'], 'Fail')
        self.assertEqual(response.data['data']['message'], 'User Registration Failed')

    @patch('api.views.SignUpSerializer')
    def test_signup_internal_server_error(self, MockSignUpSerializer):
        """
        Test internal server error during user registration.
        """
        mock_serializer_instance = MockSignUpSerializer.return_value
        mock_serializer_instance.is_valid.side_effect = Exception("Unexpected Error")

        response = self.client.post(
            self.url,
            {'idToken': 'valid_token', 'email': 'test@example.com'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['status'], 'Fail')
        self.assertEqual(response.data['data']['message'], 'Internal server error')