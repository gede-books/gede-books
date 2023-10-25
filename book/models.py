from django.db import models

class Book(models.Model):
    bookOrder = models.IntegerField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    language = models.TextField(null=True, blank=True)
    firstName = models.TextField(null=True, blank=True)
    lastName = models.TextField(null=True, blank=True)
    year = models.TextField(null=True, blank=True)
    subjects = models.TextField(null=True, blank=True)
    category= models.TextField(null=True, blank=True)