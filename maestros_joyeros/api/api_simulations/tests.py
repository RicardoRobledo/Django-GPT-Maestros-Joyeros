from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from maestros_joyeros.users.models import UserModel
from maestros_joyeros.evaluations.models import SimulationModel
from maestros_joyeros.documents.models import DocumentModel, TopicModel
from maestros_joyeros.branches.models import BranchModel

from unittest.mock import patch


class SimulationAPITestCase(APITestCase):

    def setUp(self):

        self.topic = TopicModel.objects.create(topic_name="Sample Topic")
        self.document1 = DocumentModel.objects.create(
            document_name="Doc1",
            weight=10,
            for_simulation=True,
            for_workshop=True,
            topic_id=self.topic
        )
        self.document2 = DocumentModel.objects.create(
            document_name="Doc2",
            weight=5,
            for_simulation=True,
            for_workshop=True,
            topic_id=self.topic
        )

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

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = self.refresh.access_token
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_get_simulation_unit(self):

        url = reverse('api_simulations:get_simulation')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_custom_simulation_unit(self):

        url = reverse('api_simulations:get_custom_simulation')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_type_based_simulation_unit(self):

        url = reverse('api_simulations:get_type_based_simulation')
        params = {
            'document_names': ['Proceso de ventas', 'Precios'],
            'customer_type': 'Empresarios',
            'product_name': 'Reloj'
        }
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_type_based_simulation_missing_document_unit(self):

        url = reverse('api_simulations:get_type_based_simulation')
        params = {
            'document_names': ['Doc1'],
            'customer_type': 'TypeA',
            'product_name': 'Product1'
        }
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'],
                         'There is a document that was not found')

    def test_get_type_based_simulation_missing_parameter_unit(self):

        url = reverse('api_simulations:get_type_based_simulation')

        params = {
            'document_names': ['Proceso de ventas', 'Precios'],
            'product_name': 'Product1'
        }
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_instructions_unit(self):

        url = reverse('api_simulations:retrieve_instructions')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_save_evaluation_unit(self):

        url = reverse('api_simulations:save_evaluation')

        evaluation_data = {
            '4Cs': 8,
            'Ortografía': 9,
            'Redacción': 10,
            'Promueve_acción': 10,
            'No_forzado': 10,
            'Sinceridad': 9,
            'Empatía': 10,
            'Iniciativa': 9,
            'Seguimiento': 9,
            'Cierre_conversación': 7,
            'Conversación': 'Hello, how are you?'
        }

        response = self.client.post(url, data=evaluation_data, format='json')

        saved_simulation = SimulationModel.objects.filter(
            user_id=self.user).latest('created_at')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(saved_simulation.conversation)

    def test_save_evaluation_unit(self):

        url = reverse('api_simulations:save_evaluation')

        evaluation_data = {
            '4Cs': 8,
            'Ortografía': 9,
            'Redacción': 10,
            'Promueve_acción': 10,
            'No_forzado': 10,
            'Sinceridad': 9,
            'Empatía': 10,
            'Iniciativa': 9,
            'Seguimiento': 9,
            'Cierre_conversación': 7,
            'Conversación': 'Hello, how are you?'
        }

        response = self.client.post(url, data=evaluation_data, format='json')

        saved_simulation = SimulationModel.objects.filter(
            user_id=self.user).latest('created_at')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(saved_simulation.conversation)

    def test_save_evaluation_failed_unit(self):

        url = reverse('api_simulations:save_evaluation')

        evaluation_data = {
            '4Cs': 5,
            'Ortografía': 5,
            'Redacción': 5,
            'Promueve_acción': 5,
            'No_forzado': 5,
            'Sinceridad': 2,
            'Empatía': 3,
            'Iniciativa': 2,
            'Seguimiento': 3,
            'Cierre_conversación': 5,
            'Conversación': 'Hello, how are you?'
        }

        response = self.client.post(url, data=evaluation_data, format='json')

        saved_simulation = SimulationModel.objects.filter(
            user_id=self.user).latest('created_at')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(saved_simulation.average, 5)
        self.assertTrue(saved_simulation.conversation)

    def test_save_evaluation_missing_parameter_unit(self):

        url = reverse('api_simulations:save_evaluation')

        evaluation_data = {
            '4Cs': 8,
            'Ortografía': 9,
            'Redacción': 10,
            'Promueve_acción': 10,
            'No_forzado': 10,
            'Sinceridad': 9,
            'Empatía': 10,
            # 'Iniciativa': 9,
            'Seguimiento': 9,
            'Cierre_conversación': 7,
            'Conversación': 'Hello, how are you?'
        }

        response = self.client.post(url, data=evaluation_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
