from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager


__author__ = 'Ricardo'
__version__ = '0.1'


# -------------------------------------------------------------
#                             User
# -------------------------------------------------------------


class UserManager(BaseUserManager):


    def create_user(self, username, password, email, is_staff, is_active, is_superuser=False):
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, password, email):
        return self.create_user(username, password, email, True, True, True)


class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    This model define an user

    Attributes:
        email (str): email of the user
        username (str): username of the user
        created_at (datetime): creation date
    """
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        indexes = [
            models.Index(name='user_id_idx', fields=['id']),
        ]
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'middle_name', 'last_name', 'email']

    objects = UserManager()
    name = models.CharField(unique=True, max_length=50, null=False, blank=False)
    middle_name = models.CharField(unique=True, max_length=50, null=False, blank=False,)
    last_name = models.CharField(unique=True, max_length=50, null=False, blank=False,)
    username = models.CharField(unique=True, max_length=20, null=False, blank=False,)
    email = models.EmailField(unique=True, null=False, blank=False,)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
    def __repr__(self):
        return (f'UserModel('
                f'id={self.id}, '
                f'name={self.name}, '
                f'middle_name={self.middle_name}, '
                f'last_name={self.last_name}, '
                f'username={self.username}, '
                f'email={self.email}, '
                f'is_staff={self.is_staff}, '
                f'is_active={self.is_active}, '
                f'created_at={self.created_at}, '
                f'updated_at={self.updated_at})')


class UserActionModel(models.Model):
    """
    This model define an user action

    Attributes:
        user_id (UserModel): user that made the action
        method (str): method used in the action
        path (str): path of the action
        status_code (int): status code of the action
        created_at (datetime): creation date
    """
    
    class Meta:
        verbose_name = 'user action'
        verbose_name_plural = 'user actions'
        indexes = [
            models.Index(name='user_action_user_id_idx', fields=['user_id']),
            models.Index(name='user_action_id_idx', fields=['id']),
        ]

    user_id = models.ForeignKey(UserModel, null=False, blank=False, on_delete=models.DO_NOTHING)
    method = models.CharField(max_length=10, null=False, blank=False,)
    path = models.CharField(max_length=255, null=False, blank=False,)
    status_code = models.IntegerField(null=False, blank=False,)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"UserActionModel(id={self.id}, user_id={self.user_id}, method={self.method}, path={self.path}, created_at={self.created_at})"


class WeakPointModel(models.Model):
    """
    This model define a weak point

    Attributes:
        user_id (UserModel): user that has the weak point
        weakness (str): description of the weak point
        created_at (datetime): creation date
    """
    
    class Meta:
        verbose_name = 'weak point'
        verbose_name_plural = 'weak points'
        indexes = [
            models.Index(name='weak_point_user_id_idx', fields=['user_id']),
            models.Index(name='weak_point_id_idx', fields=['id']),
        ]

    user_id = models.ForeignKey(UserModel, null=False, blank=False, on_delete=models.DO_NOTHING)
    weakness = models.CharField(max_length=100, null=False, blank=False,)
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f"WeakPointModel(id={self.id}, user_id={self.user_id}, weakness={self.weakness}, created_at={self.created_at})"


class StrongPointModel(models.Model):
    """
    This model define a strong point

    Attributes:
        user_id (UserModel): user that has the strong point
        strength (str): description of the strong point
        created_at (datetime): creation date
    """
    
    class Meta:
        verbose_name = 'strong point'
        verbose_name_plural = 'strong points'
        indexes = [
            models.Index(name='strong_point_user_id_idx', fields=['user_id']),
            models.Index(name='strong_point_id_idx', fields=['id']),
        ]

    user_id = models.ForeignKey(UserModel, null=False, blank=False, on_delete=models.DO_NOTHING)
    strength = models.CharField(max_length=100, null=False, blank=False,)
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f"StrongPointModel(id={self.id}, user_id={self.user_id}, strength={self.strength}, created_at={self.created_at})"
