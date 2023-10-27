from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    title = models.TextField(null=True, blank=True)
    language = models.TextField(null=True, blank=True)
    firstName = models.TextField(null=True, blank=True)
    lastName = models.TextField(null=True, blank=True)
    year = models.TextField(null=True, blank=True)
    subjects = models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True)
    stock = models.IntegerField(default=0)
    price = models.FloatField(default=0)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    
    def get_total(self):
        return sum(item.get_total_price() for item in self.orderitem_set.all())

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity