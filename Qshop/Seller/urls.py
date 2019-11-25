from django.urls import path,re_path
from .views import *

urlpatterns = [
    path('register/', register),
    path('index/', index),
    path('login/', login),
    path('logout/', logout),
    path('base/', base),
    path('goods_list/', goods_list),
    re_path('goods_list/(?P<type>\d{0,1})/(?P<page>\d+)/', goods_list),
    re_path('goods_status/(?P<type>\w+)/(?P<id>\d+)/', goods_status),
    # path('add_goods/',add_goods),
    path('personal_info/', PersonInfo),
    path('goods_add/',goods_add),
    path('get_code/',get_code),
    re_path('middletest/(?P<date>\w+)/',middletest),

]
