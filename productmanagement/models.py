from django.db import models

from gameadmin.models import Categories

# Create your models here.




class Stock(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.CharField(max_length=10)
    stock = models.IntegerField()
    description = models.CharField(max_length=600)
    image1 = models.ImageField(upload_to='stock_images')
    image2 = models.ImageField(upload_to='stock_images')
    image3 = models.ImageField(upload_to='stock_images')
    image4 = models.ImageField(upload_to='stock_images')
    category = models.ForeignKey(Categories,on_delete= models.CASCADE)
    proOffer  = models.IntegerField(default=5)