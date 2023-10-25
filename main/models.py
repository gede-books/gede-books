from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.TextField(null=True, blank=True)
    language = models.TextField(null=True, blank=True)
    firstName = models.TextField(null=True, blank=True)
    lastName = models.TextField(null=True, blank=True)
    year = models.TextField(null=True, blank=True)
    subjects = models.TextField(null=True, blank=True)
    category= models.TextField(null=True, blank=True)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)