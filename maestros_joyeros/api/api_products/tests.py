from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from maestros_joyeros.products.models import ProductModel
from maestros_joyeros.branches.models import BranchModel
from maestros_joyeros.users.models import UserModel


class ProductAPITestCase(APITestCase):

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
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.product1 = ProductModel.objects.create(
            product_name="Product 4",
            description="Description for product 4",
            weight=4
        )

    def test_get_products(self):

        self.product_list_url = reverse('api_products:product-list')

        response = self.client.get(self.product_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product(self):

        url = reverse('api_products:product-detail', kwargs={
                      'product_name': self.product1.product_name})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['product']['product_name'], self.product1.product_name)
        self.assertEqual(response.data['product']
                         ['description'], self.product1.description)
