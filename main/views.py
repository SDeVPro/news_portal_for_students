from django.shortcuts import render, get_object_or_404, redirect
from .models import Main 
from newss.models import News
from cat.models import Cat
from subcat.models import SubCat 
from django.contrib.auth import authenticate, login,logout 
from django.core.files.storage import FileSystemStorage
from trending.models import Trending 
import random
from random import randint 
from django.contrib.auth.models import User, Group,Permission
from manager.models import Manager 
import string 
from ipware import get_client_ip 
from ip2geotools.database.noncommercial import DbIpCity 


# Create your views here.
def home(request):
    site = Main.objects.get(pk=2)
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:3]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]
    random_object = Trending.objects.all()[randint(0,len(trending)-1)]
    return render(request,'front/home.html',{'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popnews':popnews,'popnews2':popnews2,'trending':trending,'lastnews2':lastnews2})


def about(request):
    site = Main.objects.get(pk=2)
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:3]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]
    return render(request,'front/about.html',{'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popnews':popnews,'popnews2':popnews2,'trending':trending,'lastnews2':lastnews2})

def panel(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    perm = 0 
    perms = Permission.objects.filter(user=request.user)#joriy kirayotgan user admin huquqiga ega bo'lishi kerak
    for i in perms:
        if i.codename == 'masteruser':perm=1 
    count = News.objects.count()
    rand = News.objects.all()[random.randint(0,count-1)]
    return render(request,'back/home.html',{'rand':rand})

def mylogin(request):
    if request.method == 'POST':
        utxt = request.POST.get('username')#utxt to get/receive the username , qabul qilingan usernameni olib kelsin
        ptxt = request.POST.get('password')#user paroli
        if utxt != "" and ptxt != "":
            user = authenticate(username=utxt,password=ptxt)
            if user != None:#ID raqamga ega bo'lishi kerak
                login(request,user)
                return redirect('panel')
    return render(request,'front/login.html')

def myregister(request):#registratsiya qismi
    if request.method == 'POST':
        name = request.POST.get('name')
        uname = request.POST.get('uname')#username 
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if name == "":
            msg = "Input Your Name "
            return render(request,'front/msgbox.html',{'msg':msg})
        if password1 != password2:
            msg = "Your Password Didn't Match"
            return render(request,'front/msgbox.html',{'msg':msg})
        #passwordni tekshirish 
        count1 = 0#False holatda turibti 
        count2 = 0
        count3 = 0 
        count4 = 0 
        for i in password1:
            if i>"0" and i<"9":
                count1 = 1 
            if i>"A" and i <"Z":
                count2 = 1 
            if i>"a" and i <"z":
                count3 = 1 
            if i > "!" and i < "(":
                count4 = 1 
        if count1 == 0 or count2 == 0 or count3 == 0 or count4 == 0:#bu degani parolda xato bor
            msg = "Your password is not Strong Enough"
            return render(request,'front/msgbox.html',{'msg':msg})
        if len(password1) < 8:
            msg = "Your password Must be at least 8 characters"
            return render(request,'front/msgbox.html',{'msg':msg})
        if len(User.objects.filter(username=uname)) == 0 and len(User.objects.filter(email=email))==0:
            #foydalanuvchi Ip addresini olish uchun start
            ip, is_routable = get_client_ip(request)
            if ip is None:
                ip = "0.0.0.0"
            try:
                response = DbIpCity.get(ip,api_key="free")
                country = response.country + "|" + response.city 
            except:

                country = "Unknown"
            user = User.objects.create_user(username=uname,email=email,password=password1)
            b = Manager(name=name,utxt=uname,email=email,ip=ip,country=country)
            b.save()
    return render(request,'front/login.html')

def mylogout(request):
    logout(request)
    return redirect('mylogin')

def site_setting(request):#site nastroykasi
    if not request.user.is_authenticated:
        return redirect('mylogin')
    perm = 0 
    for i in request.user.groups.all():
        if i.name == "masteruser":perm = 1 
    if perm == 0:
        error = "Access Denied"
        return render(request,'back/error.html',{'error':error})
    if request.method == 'POST':
        name = request.POST.get('name')
        tell = request.POST.get('tell')
        fb = request.POST.get('fb')
        tw = request.POST.get('tw')
        yt = request.POST.get('yt')
        link = request.POST.get('link')
        txt = request.POST.get('txt')

        if fb == "":fb="#"#hashtag avtomatik qo'yiladi
        if tw == "":tw="#"
        if yt == "":yt="#"
        if link == "":link="#"
        
        if name == "" or tell == "" or txt == "":
            error = "All fields Required"
            return render(request,'back/error.html',{'error':error})
        #logo qismi
        try:
            myfile = request.FILES['myfile']#upload file , file yuklash
            fs = FileSystemStorage()
            filename = fs.save(myfile.name,myfile)
            url = fs.url(filename)

            picurl = url 
            picname = filename 
        except:
            picurl = "-"
            picname = "-"    
    
        #ikkinchi logo, pastki qism logosi
        try:
            myfile2 = request.FILES['myfile']#upload file , file yuklash
            fs2 = FileSystemStorage()
            filename2 = fs2.save(myfile2.name,myfile2)
            url2 = fs2.url(filename)

            picurl2 = url2 
            picname2 = filename2 
        except:
            picurl2 = "-"
            picname2 = "-"  
        b = Main.objects.get(pk=2)
        b.name = name 
        b.tell = tell 
        b.fb = fb 
        b.tw = tw
        b.yt = yt 
        b.link = link 
        b.about = txt 

        if picurl != "-":b.picurl = picurl
        if picname != "-":b.picname = picname 
        if picurl2 !="-":b.picurl2 = picurl2 
        if picname2 != "-": b.picname2 = picname2 
        b.save()
    site = Main.objects.get(pk=2)
    return render(request,'back/setting.html',{'site':site})

def about_setting(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    perm = 0 
    for i in request.user.groups.all():
        if i.name == "masteruser":perms=1
    if perm == 0:#admin emas
        error = "Access Denied"#kirish o'xshamadi
        return render(request,'back/error.html',{'error':error})
    if request.method == 'POST':
        txt = request.POST.get('txt')#about us biz haqimizda degan qismiga 
        if txt == "":#bo'sh bo'lib qolsa
            error = "All Fields Required"#maydonlar bo'sh bo'lishi kerak emas
            return render(request,'back/error.html',{'error':error})
        b = Main.objects.get(pk=2)#about qismimiz va sayt nastroyka qismi primary key 2 da yotadi
        b.abouttxt = txt 
        b.save()
    about = Main.objects.get(pk=2).abouttxt
    return render(request,'back/about_setting.html',{'about':about})

def contact(request):
    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews2 = News.objects.all().order_by('-show')[:3]# - minus bu eng ko'pini olib chiqb beradi , 5687 9000 
    trending = Trending.objects.all().order_by('-pk')[:3]
    return render(request,'front/contact.html',{'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popnews2':popnews2,'trending':trending})

def change_pass(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if request.method == 'POST':
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')
        if oldpass == "" or newpass == "":
            error = "All Fields Required"
            return render(request,'back/error.html',{'error':error})
        user = authenticate(username=request.user,password=oldpass)
        if user!=None:
            if len(newpass) < 8:
                error = "Your Password Must Be At Least 8 Characters"
                return render(request,'back/error.html',{'error':error})
            count1 = 0
            count2 = 0 
            count3 = 0 
            count4 = 0 #False 
            for i in newpass:
                if i>"0" and i<"9":
                count1 = 1 
                if i>"A" and i <"Z":
                    count2 = 1 
                if i>"a" and i <"z":
                    count3 = 1 #True 
                if i > "!" and i < "(":
                    count4 = 1 
            if count1 == 1 and count2 == 1 and count3 == 1 and count4 == 1:#bu degani parolda xato bor
               user = User.objects.get(username=request.user)#username = masteruser 
               user.set_password(newpass)
               user.save()
               return redirect('mylogout')#
        else:
            error = "Your Password Is Not Correct"
            return render(request,'back/error.html',{'error':erro})
    return render(request,'back/change_pass.html')


