from django.shortcuts import render, get_object_or_404,redirect
from .models import Cat # from appni nomi .models yoki from .models import *
import csv 
from django.http import HttpResponse 


# Create your views here.
#bu yerda admin panelga chiqarib beriladigan funksiyalar yoziladi

def cat_list(request):
    #birinchi tizimga kirish kerak, demak tekshiramiz login bo'ldimi
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login tekshirish tugadi
    cat = Cat.objects.all()
    return render(request,'back/cat_list.html',{'cat':cat})

def cat_add(request):
    #bu yerda ham login tekshiriladi
    if not request.user.is_authenticated:#if not o'tmagan bo'lsa , yoki to'g'ri kelmasa holatida ishlatiladi
        return redirect('mylogin')

    if request.method == 'POST':#admin post orqali category qo'shib ketishi mumkin
        name = request.POST.get('name')#name is the field name , ism bu maydon nomi
        if name == "":
            error = "All fields required"
            return render(request,'back/error.html',{'error':error})
        if len(Cat.objects.filter(name=name)) != 0:# != tengmasmi  1 != 0 
            error = "This name user before"
            return render(request,'back/error.html',{'error':error})
        b = Cat(name=name)
        b.save()
        return redirect('cat_list')
    return render(request,'back/cat_add.html')

def export_cat_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="cat.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title','Counter'])#counter nechta belgidan iborat #100 
    for i in Cat.objects.all():
        writer.writerow([i.name,i.count])
    return response 

def import_cat_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            error = "Please Input CSV File"
            return render(request,'back/error.html',{'error':error})
        if csv_file.multiple_chunks():#hajmini o'lchaydi
            error = "File Is Too Large"
            return render(request,'back/error.html',{'error':error})
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        for line in lines:
            fields = line.split(",")
            try:
                if len(Cat.objects.filter(name=fields[0])) == 0 and fields[0]!="Title" and fields[0] != "":
                    b = Cat(name=fields[0])
                    b.save()
            except:
                print("Finish")
    return redirect('cat_list')
    







