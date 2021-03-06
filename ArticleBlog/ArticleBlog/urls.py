"""ArticleBlog URL Configuration

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
from django.urls import path,include,re_path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/',views.about, name='aboutnew'),
    path('index/',views.index),
    path('listpic/',views.listpic),
    # path('newslistpic/',views.newslistpic),
    re_path('newslistpic/(?P<page>\d+)/',views.newslistpic),
    path('base/',views.base),
    # path('addArticle/',views.addArticle),
    re_path('articleDetails/(?P<id>\d+)/',views.articleDetails),
    path('Article/',include('Article.urls')),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('requesttext/',views.requesttext),
    path('search/',views.search),
    path('register/',views.register),
    path('register1/',views.register1),
    path('ajaxdemo/',views.ajaxdemo),
    path('ajaxreq/',views.ajaxreq),
    path('ajaxregister/',views.ajaxregister),
    path('ajaxpost/',views.ajaxpost),
    path('login/',views.login),
    path('logout/',views.logout),
]
