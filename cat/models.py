from django.db import models
from __future__ import unicode_literals 
# Create your models here.

class Cat(models.Model):
    name = models.CharField(max_length=50)
    count = models.IntegerField(default=0)#bu nechta yangilik aynan shu categoryga tegishli ekanligini sonini keltirib chiqaradi

    def __str__(self):
        return self.name 
        