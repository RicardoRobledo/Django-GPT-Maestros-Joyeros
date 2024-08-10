import re

from django.core.exceptions import ValidationError
from django.db import models

from ..base.models import BaseModel


__author__ = 'Ricardo'
__version__ = '0.1'


class BranchModel(BaseModel):
    """
    This model define a branch

    Attributes:
        branch_name (str): branch name
        state (str): state of the branch
    """

    class Meta:
        verbose_name = 'branch'
        verbose_name_plural = 'branches'

    def validate_alphanumeric_with_spaces(value):

        if not re.match("^[a-zA-Z0-9\s]*$", value):

            raise ValidationError(
                'El campo solo puede contener letras, números y espacios.')

    branch_name = models.CharField(validators=[
                                   validate_alphanumeric_with_spaces], unique=True, max_length=255, null=False, blank=False)
    state = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.branch_name

    def __repr__(self):
        return f"BranchModel(branch_name={self.branch_name}, state={self.state}, created_at={self.created_at})"
