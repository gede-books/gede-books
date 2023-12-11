from django.db.models import Avg
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    bookCode = models.IntegerField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    language = models.TextField(null=True, blank=True)
    firstName = models.TextField(null=True, blank=True)
    lastName = models.TextField(null=True, blank=True)
    year = models.TextField(null=True, blank=True)
    subjects = models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True)
    stock = models.IntegerField(default=25)
    price = models.IntegerField(default=75000)
    rating = models.FloatField(default=0.0)

    def update_average_rating(self):
        avg_rating = ReviewProduct.objects.filter(product=self).aggregate(Avg('rating'))['rating__avg']
        if avg_rating is not None:
            self.rating = avg_rating
            self.save()
        else:
            self.rating = 0.0
            self.save()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def get_total(self):
        return sum(item.get_total_price() for item in self.orderitem_set.all())
    
    def get_total(self):
        return sum(item.get_total_price() for item in self.orderitem_set.all())

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity
<<<<<<< HEAD
    
class Checkout(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    payment_method = models.CharField(max_length=20)
=======

class ReviewProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    review = models.TextField(null=True, blank=True)
>>>>>>> cb2366c7a62a2fb7e99ca49eabc216a9ed650675
