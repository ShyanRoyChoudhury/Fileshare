from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Files

class GetListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('getList')  # Ensure the URL name matches your urls.py

    @patch('api.views.Files.objects.filter')
    def test_get_list_success(self, mock_files_filter):
        """
        Test successful retrieval of file list.
        """
        # Mock the Files.objects.filter method
        mock_files_filter.return_value.values.return_value = [
            {'uid': '123', 'file': 'file1.txt', 'created_at': '2023-10-01', 'name': 'File 1'},
            {'uid': '456', 'file': 'file2.txt', 'created_at': '2023-10-02', 'name': 'File 2'}
        ]

        # Mock the request.userEmail
        mock_request = MagicMock()
        mock_request.userEmail = 'test@example.com'

        # Use the client to send a POST request
        response = self.client.post(self.url, {}, format='json')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Verify the mock was called with the correct arguments
        mock_files_filter.assert_called_once_with(user='test@example.com', deleted=False)
        mock_files_filter.return_value.values.assert_called_once_with('uid', 'file', 'created_at', 'name')

    @patch('api.views.Files.objects.filter')
    def test_get_list_internal_server_error(self, mock_files_filter):
        """
        Test internal server error during file list retrieval.
        """
        # Mock the Files.objects.filter method to raise an exception
        mock_files_filter.side_effect = Exception("Unexpected Error")

        # Mock the request.userEmail
        mock_request = MagicMock()
        mock_request.userEmail = 'test@example.com'

        # Use the client to send a POST request
        response = self.client.post(self.url, {}, format='json')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response structure for error
        self.assertEqual(response.data, {
            'data': {
                'status': 'Fail',
                'data': None,
                'message': 'Internal Server Error'
            }
        })