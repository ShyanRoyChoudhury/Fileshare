from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from rest_framework import status

class VerifyMFAViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('otp_verify  ')  # Ensure the URL name matches your urls.py

    @patch('api.views.VerifyMFASerializer')
    def test_verify_mfa_success(self, mock_serializer):
        """
        Test successful OTP verification.
        """
        # Mock the VerifyMFASerializer
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.verify_mfa.return_value = True

        # Use the client to send a POST request
        response = self.client.post(self.url, {'otp': '123456'}, format='json')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'status': 'Success',
                'message': 'User 2FA enabled successfully'
            }
        })

        # Verify the mock was called with the correct arguments
        mock_serializer.assert_called_once_with(data={'otp': '123456'}, context={'userEmail': None})
        mock_serializer_instance.is_valid.assert_called_once()
        mock_serializer_instance.verify_mfa.assert_called_once()

    @patch('api.views.VerifyMFASerializer')
    def test_verify_mfa_incorrect_otp(self, mock_serializer):
        """
        Test incorrect OTP during verification.
        """
        # Mock the VerifyMFASerializer
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.verify_mfa.return_value = False

        # Use the client to send a POST request
        response = self.client.post(self.url, {'otp': '123456'}, format='json')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'status': 'Fail',
                'message': 'Incorrect OTP'
            }
        })

    @patch('api.views.VerifyMFASerializer')
    def test_verify_mfa_invalid_data(self, mock_serializer):
        """
        Test invalid data during OTP verification.
        """
        # Mock the VerifyMFASerializer to return invalid data
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.return_value = False
        mock_serializer_instance.errors = {'otp': ['Invalid OTP']}

        # Use the client to send a POST request
        response = self.client.post(self.url, {'otp': 'invalid'}, format='json')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'status': 'Fail',
                'message': 'Invalid data'
            }
        })

    @patch('api.views.VerifyMFASerializer')
    def test_verify_mfa_internal_server_error(self, mock_serializer):
        """
        Test internal server error during OTP verification.
        """
        # Mock the VerifyMFASerializer to raise an exception
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.side_effect = Exception("Unexpected Error")

        # Use the client to send a POST request
        response = self.client.post(self.url, {'otp': '123456'}, format='json')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'message': 'Internal Server Error',
                'status': 'Fail'
            }
        })