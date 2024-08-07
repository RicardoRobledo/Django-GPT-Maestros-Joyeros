from django.db import models

from maestros_joyeros.base.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator


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
    weight = models.PositiveSmallIntegerField(validators=[MinValueValidator(
        1), MaxValueValidator(10)], blank=True, null=True, default=1)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.product_name

    def __repr__(self):
        return f"ProductModel(product_name={self.product_name}, description={self.description}, weight={self.weight}, created_at={self.created_at}, updated_at={self.updated_at})"
