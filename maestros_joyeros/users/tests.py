from django.urls import reverse
from django.test import TestCase, RequestFactory, Client
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Group, Permission

from .utils.pdf_managers import create_single_report, create_branch_report

from maestros_joyeros.branches.models import BranchModel
from maestros_joyeros.users.models import UserModel
from maestros_joyeros.products.models import ProductModel


class UserTestCase(TestCase):

    def setUp(self):

        self.client = Client()

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

        self.product = ProductModel.objects.create(
            product_name="TestProduct",
            description="TestDescription"
        )

        # Add necessary permissions and groups
        self.group = Group.objects.create(name='TestGroup')
        self.add_permission = Permission.objects.get(
            codename='add_productmodel')
        self.delete_permission = Permission.objects.get(
            codename='delete_productmodel')
        self.group.permissions.add(self.add_permission, self.delete_permission)
        self.user.groups.add(self.group)
        self.user.user_permissions.add(self.delete_permission)
        self.user.save()

    def tearDown(self):
        pass

    def test_user_creation(self):

        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.username, "johnsmith")

    def test_user_update(self):

        self.user.first_name = "Jane"
        self.user.save()

        self.assertEqual(self.user.first_name, "Jane")

    def test_user_deletion(self):

        user_id = self.user.id
        self.user.delete()

        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(id=user_id)

    def test_user_search_by_username(self):

        user = UserModel.objects.get(username="johnsmith")
        self.assertEqual(user.email, "johnsmith@example.com")

    def test_user_search_by_email(self):

        user = UserModel.objects.get(email="johnsmith@example.com")
        self.assertEqual(user.username, "johnsmith")

    def test_user_can_add_product(self):

        self.assertTrue(self.user.has_perm('products.add_productmodel'))

        new_product = ProductModel.objects.create(
            product_name="New Product",
            description="New Description",
            weight=6
        )

        self.assertEqual(new_product.product_name, "New Product")
        self.assertEqual(new_product.description, "New Description")
        self.assertEqual(new_product.weight, 6)

    def test_user_can_delete_product(self):

        self.assertTrue(self.user.has_perm('products.delete_productmodel'))
        product_id = self.product.id
        self.product.delete()

        with self.assertRaises(ProductModel.DoesNotExist):
            ProductModel.objects.get(id=product_id)

    def test_user_cannot_delete_product_without_permission(self):

        # Remove deletion permission
        self.group.permissions.remove(self.delete_permission)
        self.user.user_permissions.remove(self.delete_permission)
        self.user.save()

        self.assertFalse(self.user.has_perm('products.delete_productmodel'))

        # Attempt to log in with correct credentials
        response = self.client.login(
            username='johnsmith', password='password123')

        # login succesful
        self.assertTrue(response)

        # Verify that the product still exists
        product_exists = ProductModel.objects.filter(
            id=self.product.id).exists()
        self.assertTrue(product_exists)


class PDFReportTestCase(TestCase):

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

    def test_create_single_report(self):

        total_simulations = 2

        user_simulation_evaluation = [
            {'metric_name': '4Cs', 'metric_average': 75},
            {'metric_name': 'Negociación', 'metric_average': 85}
        ]

        total_workshops = 2

        user_workshop_scores = [
            {'topic_name': 'Topic 1', 'topic_count': 1, 'topic_average': 85},
            {'topic_name': 'Topic 2', 'topic_count': 2, 'topic_average': 90}
        ]

        response = create_single_report(
            self.user, total_simulations, user_simulation_evaluation, total_workshops, user_workshop_scores)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_create_branch_report(self):

        total_simulations = 0
        user_simulation_scores = []

        total_workshops = 2
        user_workshop_evaluations = [
            {'topic_name': 'Topic 1', 'topic_count': 1, 'topic_average': 85},
            {'topic_name': 'Topic 2', 'topic_count': 2, 'topic_average': 90}
        ]

        response = create_branch_report(
            self.branch.branch_name, total_simulations, user_simulation_scores, total_workshops, user_workshop_evaluations)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')


class PDFReportAdminTest(TestCase):

    def setUp(self):

        self.client = Client()

        self.branch = BranchModel.objects.create(
            branch_name="Sample Branch",
            state="NY"
        )

        self.site = AdminSite()
        self.factory = RequestFactory()

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

    def test_generate_branch_report_pdf(self):

        # Simula una solicitud GET al panel de admin para generar un PDF
        request = self.factory.get(
            reverse('admin:generate_branch_report', args=[self.branch.branch_name]))

        # Autenticar el usuario en la solicitud
        request.user = self.user

        # Llama a la vista de generación de PDF directamente
        response = create_branch_report(
            branch_name=self.branch.branch_name,
            total_simulations=5,
            user_simulation_scores=[
                {"metric_name": "Accuracy", "metric_average": 8.5}],
            total_workshops=3,
            user_workshop_evaluations=[
                {"topic_name": "Sales", "topic_count": 2, "topic_average": 9.0}]
        )

        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename=', response['Content-Disposition'])
        self.assertGreater(len(response.content), 0)
