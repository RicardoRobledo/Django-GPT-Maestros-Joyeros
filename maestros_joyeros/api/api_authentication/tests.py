from django.urls import reverse
from django.conf import settings

from unittest.mock import patch

from rest_framework.test import APITestCase
from rest_framework import status

from maestros_joyeros.users.models import UserModel
from maestros_joyeros.branches.models import BranchModel


class GenerateGPTTokensAPITestCase(APITestCase):

    def setUp(self):

        self.branch = BranchModel.objects.create(
            branch_name="Sample Branch",
            state="NY"
        )

        self.user = UserModel.objects.create(
            first_name="John",
            middle_name="Doe",
            last_name="Smith",
            username="johnsmith",
            email="johnsmith@example.com",
            is_staff=False,
            is_active=True,
            is_superuser=False,
            password="password123",
            branch_id=self.branch
        )
        self.user.set_password('password123')
        self.user.save()

        self.valid_client_secret = settings.CLIENT_SECRET
        self.valid_client_id = settings.CLIENT_ID

    @patch('maestros_joyeros.api.api_authentication.utils.token_handlers.decode_token')
    @patch('maestros_joyeros.api.api_authentication.utils.token_handlers.create_token')
    def test_generate_gpt_tokens_authorization_code(self, mock_create_token, mock_decode_token):

        mock_decode_token.return_value = {'username': self.user.username}
        mock_create_token.return_value = {'access_token': 'new_access_token'}

        url = reverse('api_authentication:generate_gpt_tokens')
        data = {
            'grant_type': 'authorization_code',
            'client_secret': self.valid_client_secret,
            'client_id': self.valid_client_id,
            'code': 'valid_code'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['access_token'], 'new_access_token')

    @patch('maestros_joyeros.api.api_authentication.utils.token_handlers.decode_token')
    @patch('maestros_joyeros.api.api_authentication.utils.token_handlers.create_token')
    def test_generate_gpt_tokens_refresh_token(self, mock_create_token, mock_decode_token):

        mock_decode_token.return_value = {'username': self.user.username}
        mock_create_token.return_value = {'access_token': 'new_access_token'}

        url = reverse('api_authentication:generate_gpt_tokens')
        data = {
            'grant_type': 'refresh_token',
            'client_secret': self.valid_client_secret,
            'client_id': self.valid_client_id,
            'refresh_token': 'valid_refresh_token'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['access_token'], 'new_access_token')

    def test_generate_gpt_tokens_missing_parameters(self):

        url = reverse('api_authentication:generate_gpt_tokens')
        data = {
            'grant_type': 'authorization_code',
            'client_secret': self.valid_client_secret
            # Without client_id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_gpt_tokens_invalid_client_credentials(self):

        url = reverse('api_authentication:generate_gpt_tokens')
        data = {
            'grant_type': 'authorization_code',
            'client_secret': 'invalid_secret',
            'client_id': 'invalid_id',
            'code': 'valid_code'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('maestros_joyeros.api.api_authentication.utils.token_handlers.decode_token')
    def test_generate_gpt_tokens_invalid_grant_type(self, mock_decode_token):

        mock_decode_token.return_value = None

        url = reverse('api_authentication:generate_gpt_tokens')
        data = {
            'grant_type': 'invalid_grant_type',
            'client_secret': self.valid_client_secret,
            'client_id': self.valid_client_id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('maestros_joyeros.api.api_authentication.utils.token_handlers.decode_token')
    def test_generate_gpt_tokens_user_not_found(self, mock_decode_token):

        mock_decode_token.return_value = {'username': 'nonexistent_user'}

        url = reverse('api_authentication:generate_gpt_tokens')
        data = {
            'grant_type': 'authorization_code',
            'client_secret': self.valid_client_secret,
            'client_id': self.valid_client_id,
            'code': 'valid_code'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
