from django.contrib.auth.models import Group
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from maestros_joyeros.base.models import BaseModel


__author__ = 'Ricardo'
__version__ = '0.1'


# -------------------------------------------------------------
#                             User
# -------------------------------------------------------------


class UserManager(BaseUserManager):

    def create_user(self, first_name, middle_name, last_name, username, password, email, is_staff, is_active, is_superuser=False):
        user = self.model(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, middle_name, last_name, username, password, email):
        return self.create_user(first_name, middle_name, last_name, username, password, email, True, True, True)


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    This model define an user

    Attributes:
        email (str): email of the user
        username (str): username of the user
        created_at (datetime): creation date
    """

    class Meta:
        app_label = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        indexes = [
            models.Index(name='user_id_idx', fields=['id']),
        ]

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name', 'email']

    objects = UserManager()
    first_name = models.CharField(max_length=50, null=False, blank=False)
    middle_name = models.CharField(max_length=50, null=False, blank=False,)
    last_name = models.CharField(max_length=50, null=False, blank=False,)
    username = models.CharField(
        unique=True, max_length=20, null=False, blank=False,)
    email = models.EmailField(unique=True, null=False, blank=False,)
    branch_id = models.ForeignKey('branches.BranchModel', null=True, blank=False,
                                  related_name='user_branch', on_delete=models.DO_NOTHING)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",
        related_query_name="custom_user",
    )

    def __str__(self):
        return self.username

    def __repr__(self):
        return (f'UserModel('
                f'id={self.id}, '
                f'first_name={self.first_name}, '
                f'middle_name={self.middle_name}, '
                f'last_name={self.last_name}, '
                f'username={self.username}, '
                f'email={self.email}, '
                f'branch_id={self.branch_id}, '
                f'is_staff={self.is_staff}, '
                f'is_active={self.is_active}, '
                f'created_at={self.created_at}, '
                f'updated_at={self.updated_at})')


class UserActionModel(BaseModel):
    """
    This model define an user action

    Attributes:
        user_id (UserModel): user that made the action
        method (str): method used in the action
        path (str): path of the action
        status_code (int): status code of the action
        created_at (datetime): creation date
        updated_at (datetime): update date
    """

    class Meta:
        verbose_name = 'user action'
        verbose_name_plural = 'user actions'
        indexes = [
            models.Index(name='user_action_user_id_idx', fields=['user_id']),
            models.Index(name='user_action_id_idx', fields=['id']),
        ]

    method = models.CharField(max_length=10, null=False, blank=False,)
    path = models.CharField(max_length=255, null=False, blank=False,)
    status_code = models.IntegerField(null=False, blank=False,)
    user_id = models.ForeignKey(UserModel, null=False, blank=False,
                                related_name='action_users', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.path}'

    def __repr__(self):
        return f'UserActionModel(id={self.id}, user_id={self.user_id}, method={self.method}, path={self.path}, created_at={self.created_at})'
