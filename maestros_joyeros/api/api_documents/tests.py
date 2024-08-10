from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from maestros_joyeros.documents.models import DocumentModel, TopicModel
from maestros_joyeros.users.models import UserModel
from maestros_joyeros.branches.models import BranchModel

from .utils.document_handlers import get_context_documents


class DocumentAPITestCase(APITestCase):

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

        # Obtén el token de acceso
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = self.refresh.access_token

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.topic = TopicModel.objects.create(topic_name='Sample Topic')

        self.document = DocumentModel.objects.create(
            document_name="Document 1",
            content="Content for document 1",
            weight=2,
            for_workshop=True,
            for_simulation=False,
            topic_id=self.topic
        )

    def test_get_document(self):

        url = reverse('api_documents:get_document', kwargs={
                      'document_name': self.document.document_name})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['document']['document_name'], self.document.document_name)

    def test_get_nonexistent_document(self):

        url = reverse('api_documents:get_document', kwargs={
                      'document_name': 'Nonexistent Document'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HandlersAPITestCase(APITestCase):

    def setUp(self):

        self.topic1 = TopicModel.objects.create(topic_name="Test Topic 1")

        self.document = DocumentModel.objects.create(
            document_name="Test Document 1",
            topic_id=self.topic1,
            for_simulation=True,
            for_workshop=True,
            weight=1
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
        )

        self.user.set_password('password123')
        self.user.save()

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = self.refresh.access_token
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_get_context_documents(self):

        documents = get_context_documents()

        self.assertEqual(len(documents), 2)

    def test_get_document(self):

        url = reverse('api_documents:get_document', kwargs={
                      'document_name': self.document.document_name})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
