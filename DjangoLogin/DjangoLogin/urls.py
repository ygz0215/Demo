"""DjangoLogin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from .views import *
from rest_framework import  routers
routers=routers.DefaultRouter()
routers.register('goods',GoodsViewsSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',register),
    path('index/',index),
    path('login/',login),
    path('logout/',logout),
    path('base/',base),
    path('vuedemo/',vuedemo),
    path('goods_list/',goods_list),
    re_path('goods_list/(?P<type>\d{0,1})/(?P<page>\d+)/',goods_list),
    re_path('goods_status/(?P<type>\w+)/(?P<id>\d+)/',goods_status),
    re_path('goods_list_api/(?P<type>\d{0,1})/(?P<page>\d+)/',goods_list_api),
    # path('add_goods/',add_goods),
    path('goodsview/',GoodsView.as_view()),
    re_path('^API',include(routers.urls)),
    path('personal_info/',PersonInfo),

]
