import random
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from maestros_joyeros.documents.models import DocumentModel, TopicModel
from maestros_joyeros.branches.models import BranchModel
from maestros_joyeros.users.models import UserModel
from maestros_joyeros.evaluations.models import WorkshopEvaluationModel

from maestros_joyeros.api.api_documents.utils.document_handlers import get_documents_not_evaluated

from unittest.mock import patch


class WorkshopTestCase(APITestCase):

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

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = self.refresh.access_token
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

        self.topics = TopicModel.objects.all()
        self.documents = DocumentModel.objects.all()

        for _ in range(self.documents.count()-1):
            WorkshopEvaluationModel.objects.create(
                average=random.randint(2, 10), topic_id=random.choice(self.topics), user_id=self.user
            )

        self.topic1 = TopicModel.objects.create(topic_name=f"Test Topic")

        self.document1 = DocumentModel.objects.create(
            document_name=f"Test Document prim",
            content="This is a test document",
            for_workshop=True,
            weight=1,
            topic_id=self.topic1
        )

        self.document2 = DocumentModel.objects.create(
            document_name=f"Test Document sec",
            content="This is a test document",
            for_workshop=True,
            weight=1,
            topic_id=self.topic1,
        )

        self.document3 = DocumentModel.objects.create(
            document_name=f"Test Document thr",
            content="This is a test document",
            for_workshop=False,
            weight=1,
            topic_id=self.topic1,
        )

    def test_get_workshop(self):

        url = reverse('api_workshops:get_workshop')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('document', response.data)
        self.assertIn('topic', response.data)

    def test_get_specific_workshop(self):

        url = reverse('api_workshops:get_specific_workshop', args=[
                      self.document1.document_name])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('document', response.data)
        self.assertIn('topic', response.data)

    def test_get_specific_workshop_not_found(self):

        url = reverse('api_workshops:get_specific_workshop',
                      args=['Nonexistent Document'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_save_evaluation_no_average(self):

        url = reverse('api_workshops:save_evaluation',
                      args=[self.topic1.topic_name])
        data = {}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_save_evaluation(self):

        url = reverse('api_workshops:save_evaluation',
                      args=[self.topic1.topic_name])
        data = {
            'Average': 10
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['msg'], 'Evaluation of workshop saved succesfully')

    def test_save_evaluation_topic_not_found(self):

        url = reverse('api_workshops:save_evaluation',
                      args=['Nonexistent Topic'])
        data = {
            'Average': 8
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_get_custom_workshop(self):

        # Get actual date and hour
        now = timezone.now()

        # Calculate date 32 days ago
        start_date = now - timedelta(days=32)

        documents_not_evaluated = get_documents_not_evaluated(
            self.user, start_date, for_workshop=True)

        documents_not_evaluated_filtered = documents_not_evaluated.filter(
            id__in=[self.document1.id, self.document2.id]).order_by('id')

        self.assertQuerySetEqual([document_not_evaluated['id'] for document_not_evaluated in documents_not_evaluated_filtered], [
            self.document1.id, self.document2.id])

    def test_get_custom_workshop_not_for_workshop(self):

        url = reverse('api_workshops:get_specific_workshop', args=[
                      self.document3.document_name])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
