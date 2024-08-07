from django.test import TestCase

from maestros_joyeros.products.models import ProductModel


class ProductViewTestCase(TestCase):

    def setUp(self):

        self.product1 = ProductModel.objects.create(
            product_name="Product 4",
            description="Description for product 4",
            weight=4
        )

    def test_product_creation(self):

        self.assertEqual(self.product1.product_name, "Product 4")
        self.assertEqual(self.product1.description,
                         "Description for product 4")
        self.assertEqual(self.product1.weight, 4)

    def test_product_read(self):

        product = ProductModel.objects.get(id=self.product1.id)

        self.assertEqual(product.product_name, "Product 4")
        self.assertEqual(product.description, "Description for product 4")
        self.assertEqual(product.weight, 4)

    def test_product_update(self):

        self.product1.product_name = "Updated Product"
        self.product1.description = "Updated description for product"
        self.product1.weight = 5
        self.product1.save()

        updated_product = ProductModel.objects.get(id=self.product1.id)
        self.assertEqual(updated_product.product_name, "Updated Product")
        self.assertEqual(updated_product.description,
                         "Updated description for product")
        self.assertEqual(updated_product.weight, 5)

    def test_product_delete(self):

        product_id = self.product1.id
        self.product1.delete()

        with self.assertRaises(ProductModel.DoesNotExist):
            ProductModel.objects.get(id=product_id)
