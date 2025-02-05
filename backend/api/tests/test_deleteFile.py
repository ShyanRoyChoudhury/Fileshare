from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Files
import os

class DeleteFileViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('delete_file', args=['123'])  # Ensure the URL name matches your urls.py

    @patch('api.views.Files.objects.get')
    @patch('api.views.os.path.exists')
    @patch('api.views.os.remove')
    def test_delete_file_success(self, mock_os_remove, mock_os_path_exists, mock_files_get):
        """
        Test successful file deletion.
        """
        # Mock the Files.objects.get method
        mock_file_obj = MagicMock()
        mock_file_obj.file.path = '/path/to/file.txt'
        mock_files_get.return_value = mock_file_obj

        # Mock os.path.exists to return True
        mock_os_path_exists.return_value = True

        # Use the client to send a GET request
        response = self.client.get(self.url)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'status': 'Success',
                'data': None,
                'message': 'File deleted successfully'
            }
        })

        # Verify the file was deleted from the file system
        mock_os_remove.assert_called_once_with('/path/to/file.txt')

        # Verify the file was deleted from the database
        mock_file_obj.delete.assert_called_once()

    @patch('api.views.Files.objects.get')
    def test_delete_file_not_found(self, mock_files_get):
        """
        Test file not found in the database.
        """
        # Mock the Files.objects.get method to raise DoesNotExist
        mock_files_get.side_effect = Files.DoesNotExist

        # Use the client to send a GET request
        response = self.client.get(self.url)

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify the response structure
        self.assertEqual(response.data, {
            'data': {
                'status': 'Fail',
                'data': None,
                'message': 'File not found'
            }
        })

    @patch('api.views.Files.objects.get')
    @patch('api.views.os.path.exists')
    def test_delete_file_validation_error(self, mock_os_path_exists, mock_files_get):
        """
        Test validation error during file deletion.
        """
        # Mock the Files.objects.get method
        mock_file_obj = MagicMock()
        mock_file_obj.file.path = '/path/to/file.txt'
        mock_files_get.return_value = mock_file_obj

        # Mock os.path.exists to return True
        mock_os_path_exists.return_value = True

        # Mock the serializer to return invalid data
        with patch('api.views.FileDeleteSerializer') as mock_serializer:
            mock_serializer_instance = mock_serializer.return_value
            mock_serializer_instance.is_valid.return_value = False
            mock_serializer_instance.errors = {'uid': ['Invalid UUID']}

            # Use the client to send a GET request
            response = self.client.get(self.url)

            # Verify the response status code
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Verify the response structure
            self.assertEqual(response.data, {
                'data': {
                    'status': 'Fail',
                    'data': None,
                    'message': 'validation error'
                }
            })

    @patch('api.views.Files.objects.get')
    def test_delete_file_internal_server_error(self, mock_files_get):
        """
        Test internal server error during file deletion.
        """
        # Mock the Files.objects.get method to raise an exception
        mock_files_get.side_effect = Exception("Unexpected Error")

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