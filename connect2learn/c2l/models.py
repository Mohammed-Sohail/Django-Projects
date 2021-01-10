from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class c2lUser(models.Model):
    username = models.CharField(verbose_name='User Name', max_length=50,blank=False,unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone=models.CharField(verbose_name="Phone Number",max_length=12,blank=False)
    address = models.CharField(max_length=400,verbose_name="Address",null=True,blank=True)
   
    def __str__(self):
        return self.first_name+" "+self.last_name