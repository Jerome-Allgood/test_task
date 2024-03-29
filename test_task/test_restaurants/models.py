from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=15)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    tables = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f'{self.name}'

    @property
    def reserves(self):
        return self.preorder_set.filter(status='confirmed').count()

    @property
    def total_order_count(self):
        return self.preorder_set.count() + self.reserves


class PreOrder(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('declined', 'Declined')
    )

    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='new')

    def __str__(self):
        return f'Preorder #{self.id} - {self.status}'


class Reserved(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    preorder = models.OneToOneField(PreOrder, on_delete=models.CASCADE,
                                    related_name='preorder_nest')
    comment = models.TextField(max_length=1000, null=True)

    @property
    def restaurant(self):
        return self.preorder.restaurant

    @property
    def user(self):
        return self.preorder.user
