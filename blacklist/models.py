from django.db import models
from __future__ import unicode_literals 
# Create your models here.

class BlackList(models.Model):
    ip = models.CharField(max_length=10)

    def __str__(self):
        return self.ip 
        