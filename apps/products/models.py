from django.db import models

from apps.base.models import BaseModel


__author__ = 'Ricardo'
__version__ = '0.1'


class ProductModel(BaseModel):
    """
    This model define a product

    Attributes:
        product_name (str): product name
        description (str): product description
    """

    product_name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
    
    def __str__(self):
        return self.product_name

    def __repr__(self):
        return f"ProductModel(product_name={self.product_name}, description={self.description}, created_at={self.created_at}, updated_at={self.updated_at})"
