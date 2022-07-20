from django.db import models
from __future__ import unicode_literals
# Create your models here.

class News(models.Model):
    name = models.CharField(max_length=200)#yangilik nomi
    short_txt = models.TextField()#yangilik qisqacha yozuvi
    body_txt = models.TextField()#yangilik tana qismi
    date = models.CharField(max_length=12)#sanasi
    time = models.CharField(max_length=12,default="00:00")#vaqti
    picname = models.TextField()#rasm nomi
    picurl = models.TextField(default="-")#rasm urli 
    writer = models.CharField(max_length=100)#muallif
    catname = models.CharField(max_length=100,default="-")#category nomi
    catid = models.IntegerField(default=0)#category id raqami
    ocatid = models.IntegerField(default=0)#ocatid means original cat id for coun news bir nechta sanoqli yangilik original xususiyatiga ega bo'lishi mumkin
    show = models.IntegerField(default=0)#nechta ko'rilganligi yoki o'qilganligi
    tag = models.TextField(default="")#hash tag -  bu qaysi manbalarga yoki qaysi holatlarga tegishli ekanligi
    act = models.IntegerField(default=0)#bu for publish news - chop etilgan yangilikmi
    rand = models.IntegerField(default=0)#for random number of the news - bu degani yangilik random raqamlar orqali belgilanadimi

    def __str__(self):
        return self.name 
        

