from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from api.models import FileDownloadLink
from django.urls import reverse
import os


class EncryptedFileDownloadTestCase(TestCase):
    @patch('api.views.DownloadFileTempLinkSerializer')
    def test_invalid_token_permission(self, mock_serializer):
        # Mock the serializer to return invalid data
        mock_serializer.return_value.is_valid.return_value = False
        
        url = reverse('serveFiles', args=['invalid_token'])
        response = self.client.get(url, {'permission': 'read'})
        
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Validation error")



class EncryptedFileDownloadTestCase(TestCase):
    @patch('api.views.FileDownloadLink')
    def test_link_expired(self, mock_file_download_link):
        # Mock an expired link
        mock_file_download_link.objects.get.return_value.is_expired.return_value = True
        
        url = reverse('serveFiles', args=['expired_token'])
        response = self.client.get(url, {'permission': 'read'})
        
        self.assertEqual(response.status_code, 410)
        self.assertContains(response, "Download link has expired")



class EncryptedFileDownloadTestCase(TestCase):
    @patch('api.views.FileDownloadLink')
    def test_link_used(self, mock_file_download_link):
        # Mock a link that has already been used
        mock_file_download_link.objects.get.return_value.is_used = True
        
        url = reverse('serveFiles', args=['used_token'])
        response = self.client.get(url, {'permission': 'read'})
        
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "Download link has already been used")


class EncryptedFileDownloadTestCase(TestCase):
    @patch('api.views.os.path.exists')
    def test_file_not_found(self, mock_exists):
        # Mock file not existing
        mock_exists.return_value = False
        
        url = reverse('serveFiles', args=['valid_token'])
        response = self.client.get(url, {'permission': 'read'})
        
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "File not found on server")


class EncryptedFileDownloadTestCase(TestCase):
    @patch('api.views.base64.b64encode')
    @patch('api.views.open')
    @patch('api.views.FileDownloadLink.objects.get')
    def test_successful_download(self, mock_get, mock_open, mock_b64encode):
        # Mock file download link and file data
        mock_get.return_value.is_expired.return_value = False
        mock_get.return_value.is_used = False
        mock_open.return_value.__enter__.return_value.read.return_value = b"encrypted_data"
        mock_b64encode.return_value.decode.return_value = "base64_data"

        url = reverse('serveFiles', args=['valid_token'])
        response = self.client.get(url, {'permission': 'read'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Secure File Download")
        self.assertIn("base64_data", response.content.decode())
