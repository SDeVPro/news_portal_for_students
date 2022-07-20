from django.db import models
from __future__ import unicode_literals
# Create your models here.
class SubCat(models.Model):
    name = models.CharField(max_length=50)
    catname = models.CharField(max_length=50)#asosiy category ismi nomi
    catid = models.CharField()

    def __str__(self):
        return self.name 
        
