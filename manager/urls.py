from django.urls import path
from .import views#from ichki application bo'lsa to'g'ridan to'g'ri shuni viewsni olib keladi
#from app.name import views 
#<int:pk> <int:id>#pk primary key , id - identifikatsion raqam, int deb kelishidan maqsad , modellarda sonlardan tashkil 123456 , <token:token> / <str:token>, 12aa53sas54as55!@#$% 
urlpatterns = [
    path('panel/manager/list/',views.manager_list,name='manager_list'),
    path('panel/manager/del/<int:pk>/',views.manager_del,name='manager_del'),
    path('panel/manager/group/',views.manager_group,name='manager_group'),
    path('panel/manager/group/add/',views.manager_group_add,name='manager_group_add'),
    path('panel/manager/group/del/<str:name>/',views.manager_group_del,name='manager_group_del'),
    path('panel/manager/group/show/<int:pk>/',views.users_groups,name='users_groups'),
    path('panel/manager/addtogroup/<int:pk>/',views.add_users_to_groups,name='add_users_to_groups'),
    path('panel/manager/delgroup/<int:pk>/<str:name>/',views.del_users_to_groups,name='del_users_to_groups'),
    path('panel/manager/perms/',views.manager_perms,name='manager_perms'),
    path('panel/manager/perms/del/<str:name>/',views.manager_perms_del,name='manager_perms_del'),
    path('panel/manager/perms/add/',views.manager_perms_add,name='manager_perms_add'),
    path('panel/manager/perms/show/<int:pk>/',views.manager_perms,name='manager_perms'),
    path('panel/manager/delperm/<int:pk>/<str:name>/',views.users_perms_del,name='users_perms_del'),
    path('panel/manager/addperm/<int:pk>/',views.users_perms_add,name='users_perms_add'),
    path('panel/manager/addpermtogroup/<str:name>/',views.groups_perms,name='groups_perms'),
    path('panel/manager/group/delperms/<str:gname>/<str:name>/',views.groups_perms_del,name='groups_perms_del'),
    path('panel/manager/group/addperms/<str:name>/',views.groups_perms_add,name='groups_perms_add'),
    
]
