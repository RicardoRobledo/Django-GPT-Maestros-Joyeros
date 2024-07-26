from django.db import models

from apps.base.models import BaseModel


__author__ = 'Ricardo'
__version__ = '0.1'


class CustomerModel(BaseModel):
    """
    This model define a customer

    Attributes:
        customer_type (str): customer type
        description (str): customer description
    """

    customer_type = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
    
    def __str__(self):
        return self.customer_type

    def __repr__(self):
        return f"CustomerModel(customer_type={self.customer_type}, description={self.description}, created_at={self.created_at}, updated_at={self.updated_at})"
