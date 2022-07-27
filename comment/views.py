from django.shortcuts import render, get_object_or_404,redirect
from .models import Comment 
from newss.models import News 
from cat.models import Cat 
from subcat.models import SubCat 
from django.contrib.auth import authenticate,login,logout
from django.core.files.storage import FileSystemStorage 
from trending.models import Trending 
import random
from random import randint 
from django.contrib.auth.models import User, Group, Permission
from manager.models import Manager 
import string 
import datetime 


# Create your views here.

def news_cm_add(request,pk):
    if request.method == 'POST':
        now = datetime.datetime.now()#hozirgi vaqtni oladi 
        year = now.year #hozirgi vaqtdan faqat yilini olsin
        month = now.month #hozirgi vaqtdan faqat oyni olsin
        day = now.day #hozirgi vaqtdan kunini olsin , seshanba

        if len(str(day)) == 1:#agar uzunligi 1 taga teng bo'lsa, 5-kun 0 + 5 05 kun  
            day = "0"+str(day)
        if len(str(month)) == 1:#uzunligi 1 ga teng bo'lsa 
            month = "0" + str(month)#01 yanvar 02 fevral 
        today = str(year) + "/" + str(month)+"/" + str(day)#kunini oldi to'liq 2022 12 12
        time = str(now.hour) + ":" + str(now.minute)#15:15 
        cm = request.POST.get('msg')
        if request.user.is_authenticated:#user logged in 
            manager = Manager.objects.get(utxt=request.user)
            b = Comment(name=manager.name,email=manager.email,cm=cm,news_id=pk,date=today,time=tiem)#name = manager.name  means will take automatically from loggerd in user(manager) - manager.name managerni ismini ob qo'yishi kerak, qachonki u login qilgan paytda, 
            b.save()
        else:#user not logged in 
            name = request.POST.get('name')
            email = request.POST.get('email')
            b = Comment(name=name,email=email,cm=cm,news_id=pk,date=today,time=time)
            b.save()
    newsname = News.objects.get(pk=pk).name #ya'ni pk = primary  key asosiy kalit, models ni kaliti 
    return redirect('news_detail',word=newsname)

def comments_list(request):
    #login qilish kerak, admin
    if not request.user.is_authenticated:
        return redirect('mylogin')
    perm = 0 
    for i in request.user.groups.all():#foydalanuvchi guruhlari ichida yurilik
        if i.name == "masteruser":perm=1 #bu superuser 
    if perm == 0:#user superuser emas masteruser
        a = News.objects.get(pk=pk).writer
        if str(a) != str(request.user):#we can use a instead of str(a). it will not give error 
            error = "Access Denied"
            return render(request,'back/error.html',{'error':error})
    comment = Comment.objects.all()
    return render(request,'back/comments_list.html',{'comment':comment})

def comments_del(request,pk):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    perm = 0 
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1 
    if perm == 0:
        a = News.objects.get(pk=pk).writer
        if str(a) != str(request.user):
            error = "Access Denied"
            return render(request,'back/error.html',{'error':error})
    comment = Comment.objects.filter(pk=pk)
    comment.delete()
    return redirect('comments_list')

def comments_confirm(request,pk):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    perm = 0 
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1 
    if perm == 0:
        a = News.objects.get(pk=pk).writer
        if str(a) != str(request.user):
            error = "Access Denied"
            return render(request,'back/error.html',{'error':error})
    comment = Comment.objects.get(pk=pk)
    comment.status = 1 
    comment.save()
    return redirect('comments_list')



