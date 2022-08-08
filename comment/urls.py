from django.urls import path
from .import views

urlpatterns = [
    path('comment/add/news/<pk:pk>/',views.news_cm_add,name='news_cm_add'),
    path('comments/list/',views.comments_list,name='comment_list'),
    path('comments/del/<pk:pk>/',views.comments_del,name='comments_del'),
    path('comments/confirm/<pk:pk>',views.comments_confirm,name='comments_confirm'),
]