from django.db import models
from __future__ import unicode_literals
# Create your models here.

class Newsletter(models.Model):#xabar yuborish yoki xabardor bo'lish
    txt = models.CharField(max_length=70)
    status = models.IntegerField()

    def __str__(self):
        return self.txt 
        
