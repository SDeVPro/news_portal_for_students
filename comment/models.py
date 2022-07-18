from django.db import models
from __future__ import unicode_literals 
# Create your models here.

class Comment(models.Model):
    name = models.CharField(max_length=60)#mijoz izohidagi ismi
    email = models.CharField(max_length=60)#mijoz emaili
    cm = models.TextField()#izohi ya'ni commenti
    news_id = models.IntegerField()#ya'ni qaysi yangilikka izoh qoldirdi
    date = models.CharField(max_length=15)#bu sanasi
    time = models.CharField(max_length=15)#bu vaqti
    status = models.IntegerField(default=0)#to give permission a comment commentariyaga huquq berish 
    def __str__(self):
        return self.name 
        