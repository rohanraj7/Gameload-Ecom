from django.db import models

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images' , null=True)
    offer = models.IntegerField()

    def __str__(self):
        return self.name
    
class Banner(models.Model):
    image   = models.ImageField(upload_to='banner_images')

class Coupon(models.Model):
    coupon_name = models.CharField(max_length=150)
    coupon_code = models.CharField(max_length=150)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    validtill = models.DateTimeField()
    status = models.CharField(max_length=10,default=True)
    minimum_price = models.IntegerField()
    discount = models.IntegerField()

