from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from maestros_joyeros.customers.models import CustomerModel
from maestros_joyeros.branches.models import BranchModel
from maestros_joyeros.users.models import UserModel

from rest_framework_simplejwt.tokens import RefreshToken


class CustomerAPITestCase(APITestCase):

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

        self.customer1 = CustomerModel.objects.create(
            customer_type="Type A",
            description="Type A description"
        )
        self.customer2 = CustomerModel.objects.create(
            customer_type="Type B",
            description="Type B description"
        )

    def test_get_customers(self):

        url = reverse('api_customers:get_customers')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('Type A', response.data['customer_types'])
        self.assertIn('Type B', response.data['customer_types'])

    def test_get_customers_no_auth(self):

        self.client.credentials()  # Remove the token

        url = reverse('api_customers:get_customers')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
