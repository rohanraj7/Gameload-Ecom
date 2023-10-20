from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db import models
# Register your models here.

class UserManager(BaseUserManager):
    def create_user (self,fullname,phoneno,email,password=None, is_staff=False, is_active=True,is_superuser=False,is_admin=False):
        if not email:
            raise ValueError('user must have an email address')
        if not password:
            raise ValueError('user must have password')
        
        user_obj = self.model(email = self.normalize_email(email))
        user_obj.fullname = fullname
        user_obj.phoneno = phoneno
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.is_superuser = is_superuser
        user_obj.save(using=self._db)
        return user_obj
    

    def create_superuser(self,email,password=None):
        user = self.create_user(email=email,fullname=None,phoneno=None,password=password,is_superuser=True,is_admin=True,is_staff=True,is_active=True) 
        return user

class User(AbstractBaseUser):
    fullname = models.CharField(max_length=200,blank=True,null=True)
    phoneno = models.CharField(max_length=20,null=True,unique=True)
    email =models.EmailField(max_length=100,unique=True)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    def is_admin(self):
        return self.admin

    def is_active(self):
        return self.active