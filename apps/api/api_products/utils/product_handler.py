import random

from apps.products.models import ProductModel


__author__ = 'Ricardo'
__version__ = '1.0'
__all__ = ['prepare_product',]


def prepare_product():
    """
    Get all products from the database and then select one considering the weights

    :return: a random product with high weight
    """

    products = ProductModel.objects.all()

    product_names = []
    product_weights = []

    for product in products:
        product_names.append(product.product_name)
        product_weights.append(product.weight)

    product_name_selected = random.choices(product_names, weights=product_weights, k=1)[0]
    product_selected = products.filter(product_name=product_name_selected).first()

    return product_selected