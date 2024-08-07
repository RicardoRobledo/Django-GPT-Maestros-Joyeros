from django.test import TestCase

from maestros_joyeros.customers.models import CustomerModel


class CustomerModelTestCase(TestCase):

    def setUp(self):

        self.customer = CustomerModel.objects.create(
            customer_type="Regular",
            description="A regular customer"
        )

    def test_customer_creation(self):

        self.assertEqual(self.customer.customer_type, "Regular")
        self.assertEqual(self.customer.description, "A regular customer")
