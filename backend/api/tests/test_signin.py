from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status

class SignInViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('signIn')
    
    @patch('api.views.SignInSerializer')  # Mock SignInSerializer
    def test_signin_success(self, MockSignInSerializer):
        mock_serializer_instance = MockSignInSerializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.signin.return_value = {
            'accessToken': 'mock_access_token',
            'user': {'id': 1, 'name': 'Test User'}
        }
        
        response = self.client.post(self.url, {'idToken': 'valid_token'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['status'], 'Success')
        self.assertEqual(response.cookies['access_token'].value, 'mock_access_token')
    
    @patch('api.views.SignInSerializer')
    def test_signin_failure_invalid_token(self, MockSignInSerializer):
        mock_serializer_instance = MockSignInSerializer.return_value
        mock_serializer_instance.is_valid.return_value = False
        mock_serializer_instance.errors = {'idToken': ['Invalid token']}
        
        response = self.client.post(self.url, {'idToken': 'invalid_token'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Invalid token', str(response.data['data']['message']))  # Check for error message
    
    def test_signin_missing_id_token(self):
        response = self.client.post(self.url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['status'], 'Fail')
    
    @patch('api.views.SignInSerializer')
    def test_signin_registration_required(self, MockSignInSerializer):
        mock_serializer_instance = MockSignInSerializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.signin.return_value = None  # Simulating registration required
        response = self.client.post(self.url, {'idToken': 'valid_token'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['status'], 'Fail')
    
    @patch('api.views.SignInSerializer')
    def test_signin_internal_server_error(self, MockSignInSerializer):
        mock_serializer_instance = MockSignInSerializer.return_value
        mock_serializer_instance.is_valid.side_effect = Exception("Unexpected Error")
        
        response = self.client.post(self.url, {'idToken': 'valid_token'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['message'], 'Internal server error')
        self.assertEqual(response.data['data']['status'], 'Fail')
