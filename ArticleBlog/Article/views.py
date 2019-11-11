from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.


def index(request):
    return HttpResponse('子应用的index')

def add(request):
    return HttpResponse('添加')

def select(request):
    # article=Article.objects.get(title='西游记')
    # author=article.author
    # print(author.name)

    # author=Author.objects.get(name='琼瑶')
    # article=author.article_set.all().values('title')
    # print(article)

    # author=Author.objects.filter(gender=0).first()
    # article=author.article_set.all()
    # print(article)

    # article=Article.objects.get(title='窗外')
    # type=article.type.all().values('name','description')
    # print(type)

    # type=Type.objects.filter(name='言情').first()
    # article=type.article_set.all().values('title')
    # print(article)

    # author=Author.objects.get(name='吴承恩')
    # article=author.article_set.get()
    # type=article.type.values('name')

    # type=Type.objects.filter(name='言情').first()
    # article=type.article_set.all().first()
    # author=article.author.name

    # print(author)


    # print(type)



    return HttpResponse('查询')

def update(request):
    return HttpResponse('修改')

def delete(request):
    return HttpResponse('删除')