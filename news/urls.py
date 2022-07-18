
from django.contrib import admin
from django.urls import path,include 
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('main.urls')),
    path('',include('newss.urls')),
    path('',include('cat.urls')),
    path('',include('subcat.urls')),
    path('',include('contactform.urls')),
    path('',include('trending.urls')),
    path('',include('manager.urls')),
    path('',include('newsletter.urls')),
    path('',include('comment.urls')),
    path('',include('blacklist.urls')),
]

if settings.DEBUG: #settings dagi debug true turgan bo'lsa
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
