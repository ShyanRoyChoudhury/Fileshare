from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from rest_framework import status
import pyotp
import qrcode
import io
import base64
from ..models import User

class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('profile_view')  # Ensure the URL name matches your urls.py

    @patch('api.views.User.objects.filter')
    @patch('api.views.pyotp.random_base32')
    @patch('api.views.pyotp.totp.TOTP')
    @patch('api.views.qrcode.make')
    def test_profile_view_success(self, mock_qrcode_make, mock_totp, mock_random_base32, mock_user_filter):
        """
        Test successful retrieval of user profile and MFA QR code.
        """
        # Mock the User.objects.filter method
        mock_user = MagicMock()
        mock_user.email = 'test@example.com'
        mock_user.name = 'Test User'
        mock_user.mfa_secret = None
        mock_user.mfa_enabled = False
        mock_user_filter.return_value.first.return_value = mock_user

        # Mock pyotp.random_base32 to return a fixed secret
        mock_random_base32.return_value = 'random_secret'

        # Mock pyotp.totp.TOTP to return a provisioning URI
        mock_totp_instance = MagicMock()
        mock_totp_instance.provisioning_uri.return_value = 'otpauth://totp/Fileshare:test@example.com?secret=random_secret&issuer=Fileshare'
        mock_totp.return_value = mock_totp_instance

        # Mock qrcode.make to return a dummy QR code
        mock_qr = MagicMock()
        mock_qrcode_make.return_value = mock_qr

        # Mock the BytesIO buffer and base64 encoding
        mock_buffer = io.BytesIO()
        mock_qr.save.return_value = None
        mock_buffer.getvalue.return_value = b'dummy_qr_code'
        with patch('api.views.io.BytesIO', return_value=mock_buffer):
            with patch('api.views.base64.b64encode', return_value=b'dummy_qr_code_base64'):
                # Use the client to send a GET request
                response = self.client.get(self.url)

                # Verify the response status code
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                # Verify the response structure
                self.assertEqual(response.data, {
                    'data': {
                        'status': 'Success',
                        'qr_code': 'data:image/png;base64,dummy_qr_code_base64',
                        'email': 'test@example.com',
                        'name': 'Test User',
                        'isMFAEnabled': False
                    }
                })

                # Verify the mock was called with the correct arguments
                mock_user_filter.assert_called_once_with(email='test@example.com', deleted=False)
                mock_random_base32.assert_called_once()
                mock_totp.assert_called_once_with('random_secret')
                mock_totp_instance.provisioning_uri.assert_called_once_with(
                    name='test@example.com',
                    issuer_name='Fileshare'
                )
                mock_qrcode_make.assert_called_once_with('otpauth://totp/Fileshare:test@example.com?secret=random_secret&issuer=Fileshare')
                mock_qr.save.assert_called_once_with(mock_buffer, format='PNG')

    @patch('api.views.User.objects.filter')
    def test_profile_view_internal_server_error(self, mock_user_filter):
        """
        Test internal server error during profile retrieval.
        """
        # Mock the User.objects.filter method to raise an exception
        mock_user_filter.side_effect = Exception("Unexpected Error")

        # Use the client to send a GET request
        response = self.client.get(self.url)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'message': 'Internal Server Error',
                'status': 'Fail'
            }
        })