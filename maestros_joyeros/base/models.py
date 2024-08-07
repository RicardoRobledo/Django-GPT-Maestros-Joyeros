from django.db import models


class BaseModel(models.Model):
    """
    This model define a base model

    Attributes:
        created_at (datetime): creation date
        updated_at (datetime): update date
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
