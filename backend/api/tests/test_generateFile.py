from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from ..models import Files, FileDownloadLink

class GenerateLinkViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('generate_file_link', args=['123'])  # Ensure the URL name matches your urls.py

    @patch('api.views.Files.objects.filter')
    @patch('api.views.FileDownloadLink.objects.create')
    def test_generate_link_success(self, mock_file_download_link_create, mock_files_filter):
        """
        Test successful generation of a download link.
        """
        # Mock the Files.objects.filter method
        mock_file = MagicMock()
        mock_file.uid = '123'
        mock_file.key = 'file_key'
        mock_files_filter.return_value.first.return_value = mock_file

        # Mock the FileDownloadLink.objects.create method
        mock_temp_link = MagicMock()
        mock_temp_link.token = 'temp_token'
        mock_temp_link.expires_at = timezone.now() + timedelta(hours=24)
        mock_temp_link.permission = 'read'
        mock_file_download_link_create.return_value = mock_temp_link

        # Use the client to send a POST request with query parameters
        response = self.client.post(f"{self.url}?permission=read")

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'status': 'Success',
            'data': {
                'download_link': 'http://localhost:8000/api/serveFiles/temp_token?permission=read#key=file_key',
                'expires_at': mock_temp_link.expires_at,
                'permission': 'read'
            }
        })

        # Verify the mock was called with the correct arguments
        mock_files_filter.assert_called_once_with(uid='123', deleted=False)
        mock_file_download_link_create.assert_called_once_with(
            file=mock_file,
            expires_at=mock_temp_link.expires_at,
            permission='read'
        )

    @patch('api.views.Files.objects.filter')
    def test_generate_link_file_not_found(self, mock_files_filter):
        """
        Test file not found in the database.
        """
        # Mock the Files.objects.filter method to return None
        mock_files_filter.return_value.first.return_value = None

        # Use the client to send a POST request
        response = self.client.post(f"{self.url}?permission=read")

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'status': 'Fail',
                'message': 'File not found'
            }
        })

    @patch('api.views.GenerateFileLinkSerializer')
    def test_generate_link_validation_error(self, mock_serializer):
        """
        Test validation error during link generation.
        """
        # Mock the serializer to return invalid data
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.return_value = False
        mock_serializer_instance.errors = {'uid': ['Invalid UUID']}

        # Use the client to send a POST request
        response = self.client.post(f"{self.url}?permission=invalid")

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'status': 'Fail',
                'message': 'validation error'
            }
        })

    @patch('api.views.Files.objects.filter')
    def test_generate_link_internal_server_error(self, mock_files_filter):
        """
        Test internal server error during link generation.
        """
        # Mock the Files.objects.filter method to raise an exception
        mock_files_filter.side_effect = Exception("Unexpected Error")

        # Use the client to send a POST request
        response = self.client.post(f"{self.url}?permission=read")

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'status': 'Fail',
                'message': 'Internal server Error'
            }
        })