from django.db import models
from gameuser.models import User
from productmanagement.models import Stock

# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    productid = models.ForeignKey(Stock, on_delete=models.CASCADE)
    productname = models.CharField(max_length=200)
    price = models.IntegerField(null=True)
    image = models.ImageField(upload_to='wishlist_images')
    description = models.CharField()


class Cart(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    productid = models.ForeignKey(Stock, on_delete=models.CASCADE)
    productname = models.CharField()
    price = models.IntegerField(null=True)
    image = models.ImageField(upload_to='Cart_images')
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField


class Guestcart(models.Model):
    userreference      = models.CharField(max_length=200,null=True)
    productid          = models.ForeignKey(Stock,on_delete= models.CASCADE)
    productname        = models.CharField(max_length=200)
    price              = models.IntegerField(null=True)
    image              = models.ImageField(upload_to='pics')
    quantity           = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField



