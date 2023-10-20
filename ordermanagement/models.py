from django.db import models
from gameuser.models import User
from productmanagement.models import Stock
# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, default=None)
    lastname = models.CharField(max_length=200, default=None)
    state = models.CharField(max_length=200, default=None)
    address = models.CharField(max_length=500, default=None)
    city = models.CharField(max_length=100, default=None)
    postcode = models.CharField(max_length=20)
    phoneno = models.CharField(max_length=20)
    email = models.EmailField()



class Myorders(models.Model):
    userid    = models.ForeignKey(User,on_delete=models.CASCADE)
    productid = models.ForeignKey(Stock,on_delete= models.CASCADE)
    address   = models.ForeignKey(Address,on_delete=models.CASCADE)
    quantity  = models.IntegerField()
    amount    = models.CharField(max_length=10,null=True)
    method    = models.CharField(max_length=100,null=True)
    productname=models.CharField(max_length=100,null=True)
    image     = models.ImageField(upload_to='order_images')
    status    = models.BooleanField(default=True)
    totalamount=models.IntegerField()
    orderid   = models.CharField(max_length=150,default="1")
    orderdate = models.DateTimeField(auto_now_add=True, null=True)
    orderstatus=models.CharField(max_length=50,default='Placed')


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paymentid = models.CharField(max_length=150)
    paymentmethod = models.CharField(max_length=150)
    totalamount = models.IntegerField()
    status = models.CharField(max_length=100,default='True',null=True)
    orderid = models.CharField(max_length=200)
