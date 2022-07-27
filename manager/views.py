from django.shortcuts import render, get_object_or_404,redirect
from .models import Manager
from newss.models import News
from cat.models import Cat 
from subcat.models import SubCat 
from django.contrib.auth import authenticate,login, logout
from django.core.files.storage import FileSystemStorage
from trending.models import Trending
import random 
from random import randint 
from django.contrib.auth.models import User,Group,Permission
from django.contrib.contenttypes.models import ContentType

# Create your views here.

def manager_list(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    perm = 0 
    for i in request.user.groups.all():
        if i.name == 'masteruser':perm = 1 
    if perm == 0:
        error = "Access denied"
        return render(request,'back/error.html',{'error':error})
    manager = Manager.objects.all().exclude(utxt="sardor")#
    return render(request,'back/manager_list.html',{'manager':manager})

def manager_del(request,pk):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    perm = 0 
    for i in request.user.groups.all():
        if i.name == 'masteruser':perm = 1
    if perm == 0:
        error = "Access Denied"
        return render(request,'back/error.html',{'error':error})
    manager = Manager.objects.get(pk=pk)#sardor ni o'chirmoqchi bo'lsam demak sardorni olib kelishim kerak va uni o'chirishim kerak
    b = User.objects.filter(usernmae=manager.utxt)
    b.delete()
    manager.delete()
    return redirect('manager_list')