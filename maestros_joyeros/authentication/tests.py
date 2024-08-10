from django.test import TestCase, Client
from django.urls import reverse

from maestros_joyeros.users.models import UserModel
from maestros_joyeros.branches.models import BranchModel


class LoginViewTestCase(TestCase):

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

    def test_login_success(self):

        response = self.client.post(reverse('app_authentication:login'), {
            'username': 'johnsmith',
            'password': 'password123',
            'callback_url': 'prueba'
        })

        self.assertEqual(response.status_code, 302)

    def test_login_failure(self):

        response = self.client.post(reverse('app_authentication:login'), {
            'username': 'wrongtestuser',
            'password': 'wrongpassword',
            'callback_url': 'prueba'
        })

        self.assertEqual(response.status_code, 401)
