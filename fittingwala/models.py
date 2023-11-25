import random

from django.db import models
from django.contrib.auth.models import AbstractUser


class FitUser(AbstractUser):
    mobile = models.CharField(max_length=10, null=True, blank=True)
    verification_code = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk:
            # generate random verification code
            self.verification_code = random.randint(1000, 9999)
            self.set_password(self.password)

        super(FitUser, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category', null=True, blank=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    price_map = models.JSONField(null=True, blank=True)
    size = models.JSONField(null=True, blank=True)
    brand = models.CharField(max_length=50, null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
