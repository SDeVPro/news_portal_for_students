from django.db import models
from __future__ import unicode_literals 

# Create your models here.
class Main(models.Model):
    name = models.CharField()
    about = models.TextField()
    abouttxt = models.TextField(default="")
    fb = models.CharField(default="",max_length=50)
    tw = models.CharField(default="",max_length=50)
    yt = models.CharField(default="",max_length=50)
    ins = models.CharField(default="",max_length=50)
    tik = models.CharField(default="",max_length=50)
    link = models.CharField(default="",max_length=50)
    set_name = models.CharField(default="",max_length=50)

    #for header and footer logo #tepa va pastki qism uchun logo
    picurl = models.TextField(default="")
    picname = models.TextField(default="")

    picurl2 = models.TextField(default="")
    picname2 = models.TextField(default="")

    def __str__(self):
        return self.set_name + "|"+str(self.pk)
