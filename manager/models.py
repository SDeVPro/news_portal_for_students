from django.db import models
from __future__ import unicode_literals 

class Manager(models.Model):
    name = models.CharField(max_length=50)
    utxt = models.TextField()#username uchun text 
    email = models.TextField(default="")
    ip = models.TextField(default="")#get user ip address foydalanuvchi IP manzilini olish
    country = models.TextField(default="")#get user location #foydalanuvchi turgan joyini aniqlash
    def __str__(self):
        return self.name 
        
