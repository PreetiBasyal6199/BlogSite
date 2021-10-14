from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django import forms
# from .forms import UserRegisterForm
from django.contrib.auth.base_user import BaseUserManager
from django.urls.base import reverse
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username=None
    full_name=models.CharField(max_length=50,blank=False)
    email=models.EmailField(unique=True)
    objects=UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


CATAGORIES = [
    ('Travel', 'Travel'),
    ('Food', 'Food'),
    ('History', 'History'),
    ('Education', 'Education'),
    ('Movies', 'Movies'),
]

class blog(models.Model):
    title = models.CharField(max_length=50)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    catagory=models.CharField(choices=CATAGORIES,max_length=50)
    description=models.TextField(max_length=10000)
    post_date=models.DateTimeField(auto_now=True,auto_now_add=False)

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog instance.
        """
        return reverse('view_blog', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.username

