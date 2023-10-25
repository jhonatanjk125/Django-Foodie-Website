from xml.etree.ElementTree import TreeBuilder
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('An email address is required to create the account')
        if not username:
            raise ValueError('You must have a username to create an account')
        
        user=self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    RESTAURANT = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (RESTAURANT, 'Restaurant'),
        (CUSTOMER, 'Customer'),
    )

    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=13, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # Required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True
