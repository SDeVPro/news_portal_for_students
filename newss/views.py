from django.shortcuts import render, get_object_or_404,redirect
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime 
from subcat.models import SubCat 
from cat.models import Cat 
from trending.models import Trending 
import random
from comment.models import Comment 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#paginatsiya  - bu nima?, paginatsiyamiz bir sahifani o'zidan keyingi sahifaga o'tganda ma'lumotlar yo'qotishsiz yangi ma'lumotlarni olib kelish

# Create your views here.

def news_detail(request,id):#yangilik batafsil qismiga o'tish
    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    shownews = News.objects.filter(id=id)
    popnews = News.objects.all().order_by('-show') 
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trenging.objects.all().order_by('-pk')[:3]
    tagname = News.objects.get(id=id).tag
    tag = tagname.split(',')

    try:
        mynews = News.objects.get(id=id)
        mynews.show = mynews.show + 1
        mynews.save()
    except:
        print("Cat't Add Show")
    code = News.objects.get(id=id).pk
    comment = Comment.objects.filter(news_id=code,status=1).order_by('-pk')[:3]
    cmcount = len(comment)
    link = "/urls/"+str(News.objects.get(id=id).rand)#For QR Code
    return render(request,'front/news_detail.html',{'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'shownews':shownews,'popnews':popnews,'popnews2':popnews2,'tag':tag,'trending':trending,'code':code,'comment':comment,'cmcount':cmcount,'link':link})

def news_detail_short(request,pk):
    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    shownews = News.objects.filter(rand=pk)#random holatda yangiliklarni ko'rsatib turish
    popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:3]

    tagname = News.objects.get(rand=pk).tag
    tag = tagname.split(',')
    try:
        mynews = News.objects.get(rand=pk)
        mynews.show = mynews.show + 1 
        mynews.save()
    except:
        print("Can't Add Show")
    link = "/urls/"+str(News.objects.get(name=pk).rand)
    return render(request,'front/news_detail.html',{'site':site,'news':news,'cat':cat,'subcat':subcat,'lastname':lastname,'shownews':shownew,'popnews':popnews,'popnews2':popnews2,'tag':tag,'trending':trending,'link':link})

def news_list(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    perm = 0 
    for i in request.user.groups.all():
        if i.name == "masteruser":perm=1
    if perm == 0:#faqat yozuvchini o'ziga ya'ni muallifga tegishli bo'lgan yangilik
        news = News.objects.filter(writer=request.user)
    elif perm == 1:#huquqi admin bo'lsa
        newss = News.objects.all()
        #pagination begin 
        paginator = Paginator(newss,7)#yangiliklarni bir pagega bir sahifaga 7 tadan taxlab olib kelsin
        page = request.GET.get('page')#2 page bossam 2 pageni olib kelsin
        try:
            news = paginator.page(page)
        except EmptyPage:
            news = paginator.page(paginator.num_page)
        except PageNotAnInteger:
            news = paginator.page(1)

        return render(request,'back/news_list.html',{'news':news})
    
def news_add(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day 
    if len(str(day)) == 1:
        day = "0" + str(day)#7 07 
    if len(str(month))==1:
        month = "0" + str(month)# 2 02 
    today = str(year)+"/"+str(month)+"/"+str(day)
    time = str(now.hour)+":"+str(now.minute)
    #random raqam yangilik uchun son
    date = str(year)+str(month)+str(day)
    randint = str(random.randint(1000,9999))
    rand = date + randint 
    rand = int(rand)
    while len(News.objects.filter(rand=rand))!=0:
        randint = str(random.randint(1000,9999))
        rand = date + randint 
        rand = int(rand)
    cat = SubCat.objects.all()
    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscat')
        tag = request.POST.get('tag')
        if newstitle == "" or newstxtshort == "" or newstxt == "" or newscat == "":
            error = "All Fields Required"
            return render(request,'back/error.html',{'error':error})
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name,myfile)
            url = fs.url(filename)
            if str(myfile.content_type).startswith("image"):
                if myfile.size<50000000:
                    newsname = SubCat.objects.get(pk=newsid).name
                    ocatid = SubCat.objects.get(pk=newsid).catid
                    b = News(name=newstitle,short_txt=newstxtshort,body_txt=newstxt,date=today,picname=filename,picurl=url,writer=request.user,catname=newsname,catid=newsid,show=0,time=time,ocatid=ocatid,tag=tag,rand=rand)
                    b.save()
                    count = len(News.objects.filter(ocatid=ocatid))
                    b.Cat.objects.get(pk=ocatid)
                    b.count = count 
                    b.save()
                    return redirect('news_list')
                else:
                    fs = FileSystemStorage()
                    fs.delete(filename)
                    error = "Your File Is Bigger Than 5MB"
                    return render(request,'back/error.html',{'error':error})
            else:
                fs = FileSystemStorage()
                fs.delete(filename)
                error = "Your File Not Supported"
                return render(request,'back/error.html',{'error':error})
        except:
            error = "Please Input Your Image"
            return render(request,'back/error.html',{'error':error})
    return render(request,'back/news_add.html',{'cat':cat})
    