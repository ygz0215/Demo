from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from Article.models import *
from  django.core.paginator import Paginator

def loginvalid(func):
    def inner(request,*args,**kwargs):
        username=request.COOKIES.get('username')
        username_session=request.session.get('username')
        print(username_session)
        if username == username_session:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return inner

@loginvalid
def about(request):
    return render(request,'about.html')

@loginvalid
def index(request):

    newarticle=Article.objects.order_by('-date')[:6]
    recommendarticle=Article.objects.filter(recommend=1)[:7]
    clickarticle=Article.objects.order_by('-click')[:12]
    return render(request,'index.html',locals())

def listpic(request):

    return render(request,'listpic.html')

def newslistpic(request,page):
    page=int(page)
    article=Article.objects.all()
    paginator=Paginator(article,6)
    page_obj=paginator.page(page)


    number=page_obj.number
    start=number-3
    end=number+2
    page_range=paginator.page_range[start:end]
    if number <=2:
        start=0
        end=5
    if number >=paginator.num_pages-2:
        end=paginator.num_pages
        start=end-5
    page_range=paginator.page_range[start:end]




    return render(request,'newslistpic.html',locals())

def base(request):
    return render(request,'base.html')

def articleDetails(request,id):
    id=int(id)
    article=Article.objects.get(id=id)
    article.click+=1
    article.save()
    return render(request,'articledetails.html',locals())

def addArticle(request):
    author = Author.objects.filter().first() ## 查询第一条数据
    type = Type.objects.filter().first()
    for one in range(100):
        article = Article()
        article.title = "title_%s" % one
        article.content = "content_%s" % one
        article.description = "description_%s" % one
        article.author = author
        article.save()
        article.type.add(type)
        article.save()
    return HttpResponse("增加数据")

def fytest(request):
    ### 分页的方法
    article = Article.objects.all().order_by("id")
    # print (aricle)
    paginator = Paginator(article,5) ## 设置每一页显示多少条数据 返回是一个 paginator对象
    # # print (paginator)
    # print (paginator.count) ## 数据总条数
    # print (paginator.num_pages) ## 总页数 102/5
    # print (paginator.page_range) ### 页码的返回
    # range(start,end)
    page_obj = paginator.page(10) ### 指定页码的一个对象
    # <Page 2 of 21>
    # print (page_obj) ##

    # print (type(page_obj))
    # for one in page_obj: ## one 是每一页的数据
    # print (one)
    # print (one.title)
    # print(page_obj.number) ## 当前页码
    # print (page_obj.has_next()) ## 判断是否有下一页 返回布尔
    # print (page_obj.has_previous()) ## 判断是否有 上一页
    # print (page_obj.has_other_pages()) ## 判断是否有其他页
    # print(page_obj.next_page_number()) ## 下一页的页码
    # print(page_obj.previous_page_number()) ## 上一页的页码
    return HttpResponse("fenye test")


def requesttext(request):
    print(request.COOKIES)
    print(request.GET)


    return HttpResponse('requesttext')


def search(request):
    searchkey=request.GET.get('search')
    article=[]
    if searchkey:
        article=Article.objects.filter(title__icontains=searchkey)
    return render(request,'search.html',locals())

from Article.form import UserForm
def register(request):
    register_form=UserForm()
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username and password:
            flag=User.objects.filter(name=username).exists()
            if not flag:
                user=User()
                user.name=username
                user.password=setPassword(password)
                user.save()
                result='注册成功'
            else:
                result='用户已存在'
        else:
            result='用户名名密码不能为空'

    return render(request,'register.html',locals())

def register1(request):
    if request.method=='POST':
        name=request.POST.get('username')
        password=request.POST.get('password')
        if name and password:
            if User.objects.filter(name=name).exists():
                result = '用户已经存在'
            else:
                user = User()
                user.name = name
                user.password = password
                user.save()
                result='注册成功'
        else:
            result='用户名密码不能为空'

    return render(request,'register.html',locals())

def ajaxdemo(request):

    return render(request,'ajaxdemo.html')


from django.http import JsonResponse
def ajaxreq(request):
    username=request.GET.get('username')
    password=request.GET.get('password')
    result={'code':10000,'msg':''}
    if username and password:
        if User.objects.filter(name=username,password=password).exists():
            result['msg']='用户存在'
        else:
            result['msg']='用户不存在'
            result['code']=10001
    else:
        result['msg']='账号密码不能为空'
        result['code']='10002'
    return JsonResponse(result)



import hashlib
def setPassword(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result

def ajaxregister(request):

    return render(request,'ajaxpost.html')

def ajaxpost(request):

    # result={'code':10000,'msg':''}
    # print(request.GET)
    # username=request.POST.get('username')
    # password=request.POST.get('password')
    # if username and password:
    #     flag=User.objects.filter(name=username).exists()
    #     if flag:
    #         result={'code':10002,'msg':'该用户已存在'}
    #     else:
    #         User.objects.create(name=username,password=password)
    # else:
    #     result={"code": 10001, "msg": "参数为空"}
    result={'code':10000,'msg':''}
    username=request.POST.get('username')
    password=request.POST.get('password')
    if username and password:
        if User.objects.filter(name=username).exists():
            result={'code':10002,'msg':'用户已存在'}
        else:
            User.objects.create(name=username,password=password)
            result={'code':10000,'msg':'用户创建成功'}
    else:
        result={'code':10001,'msg':'参数为空'}
    return JsonResponse(result)

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username and password:
            user=User.objects.filter(name=username,password=password).exists()
            if user:
                response= HttpResponseRedirect('/index')
                response.set_cookie('username',username)
                request.session['username']=username
                return response
        else:
            return HttpResponse('用户名密码为空')

    return render(request,'login.html')

def logout(request):
    response=HttpResponseRedirect('/login')
    response.delete_cookie('username')
    del request.session['username']
    return response


