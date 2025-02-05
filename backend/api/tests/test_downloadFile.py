from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.base import ContentFile
from django.http import FileResponse
from ..models import Files
import os

class DownloadFileViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('download_file', args=['123'])  # Ensure the URL name matches your urls.py

    @patch('api.views.Files.objects.filter')
    @patch('api.views.os.path.exists')
    @patch('api.views.EncryptionHandler')
    def test_download_file_success(self, mock_encryption_handler, mock_os_path_exists, mock_files_filter):
        """
        Test successful file download.
        """
        # Mock the Files.objects.filter method
        mock_file_obj = MagicMock()
        mock_file_obj.file.path = '/path/to/file.txt'
        mock_file_obj.name = 'file.txt'
        mock_files_filter.return_value.first.return_value = mock_file_obj

        # Mock os.path.exists to return True
        mock_os_path_exists.return_value = True

        # Mock the EncryptionHandler
        mock_decryption_handler_instance = mock_encryption_handler.return_value
        mock_decryption_handler_instance.decrypt_file.return_value = b'decrypted content'

        # Use the client to send a GET request
        response = self.client.get(self.url)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response is a FileResponse
        self.assertIsInstance(response, FileResponse)

        # Verify the response headers
        self.assertEqual(response['Content-Type'], 'application/octet-stream')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="file.txt"')
        self.assertEqual(response['Content-Length'], '17')  # Length of 'decrypted content'

    @patch('api.views.Files.objects.filter')
    def test_download_file_not_found(self, mock_files_filter):
        """
        Test file not found in the database.
        """
        # Mock the Files.objects.filter method to return None
        mock_files_filter.return_value.first.return_value = None

        # Use the client to send a GET request
        response = self.client.get(self.url)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'status': 'Fail',
                'message': 'File not found'
            }
        })

    @patch('api.views.Files.objects.filter')
    @patch('api.views.os.path.exists')
    def test_download_file_not_found_on_server(self, mock_os_path_exists, mock_files_filter):
        """
        Test file not found on the server.
        """
        # Mock the Files.objects.filter method
        mock_file_obj = MagicMock()
        mock_file_obj.file.path = '/path/to/file.txt'
        mock_files_filter.return_value.first.return_value = mock_file_obj

        # Mock os.path.exists to return False
        mock_os_path_exists.return_value = False

        # Use the client to send a GET request
        response = self.client.get(self.url)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'status': 'Fail',
                'message': 'File not found on server'
            }
        })

    @patch('api.views.Files.objects.filter')
    @patch('api.views.os.path.exists')
    @patch('api.views.EncryptionHandler')
    def test_download_file_decryption_error(self, mock_encryption_handler, mock_os_path_exists, mock_files_filter):
        """
        Test decryption error during file download.
        """
        # Mock the Files.objects.filter method
        mock_file_obj = MagicMock()
        mock_file_obj.file.path = '/path/to/file.txt'
        mock_files_filter.return_value.first.return_value = mock_file_obj

        # Mock os.path.exists to return True
        mock_os_path_exists.return_value = True

        # Mock the EncryptionHandler to raise an exception
        mock_decryption_handler_instance = mock_encryption_handler.return_value
        mock_decryption_handler_instance.decrypt_file.side_effect = Exception("Decryption error")

        # Use the client to send a GET request
        response = self.client.get(self.url)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'message': 'Error decrypting file'
            }
        })

    @patch('api.views.Files.objects.filter')
    def test_download_file_internal_server_error(self, mock_files_filter):
        """
        Test internal server error during file download.
        """
        # Mock the Files.objects.filter method to raise an exception
        mock_files_filter.side_effect = Exception("Unexpected Error")

        # Use the client to send a GET request
        response = self.client.get(self.url)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'status': 'Fail',
                'data': None,
                'message': 'Internal Server Error'
            }
        })