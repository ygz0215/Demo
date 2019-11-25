from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from CeleryTask.tasks import Test
from django.views import View
import json


# Create your views here.

# def index(request):
#
#     return HttpResponse('index')
def LoginValid(func):
    def inner(request,*args,**kwargs):
        email=request.COOKIES.get('email')
        email_session=request.session.get('email')
        cookie_username=request.COOKIES.get('username')
        if email and email_session and email==email_session:
            flag=LoginUser.objects.filter(username=cookie_username,email=email,user_type=0).exists()
            if flag:
                return func(request,*args,**kwargs)
            else:
                return HttpResponseRedirect('/seller/login')
        else:
            return HttpResponseRedirect('/seller/login/')
    return inner


import datetime
def register(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    repassword=request.POST.get('repassword')
    code=request.POST.get('code')
    if email and password and repassword and code:
        if password != repassword:
            result='密码不一致'
        else:
            flag = LoginUser.objects.filter(email=email).exists()
            if flag:
                result='用户已存在'
            else:
                print('abcccc')
                validcode=ValidCode.objects.filter(user=email,code=code).order_by('id').first()
                if validcode:
                    now_time=datetime.datetime.now()
                    db_time=validcode.date
                    t = (now_time - db_time).total_seconds()
                    print(t)
                    if t>120:
                        result='验证码已失效 请重新获取'
                    else:
                        LoginUser.objects.create(email=email,username=email,password=setPassword(password),user_type=0)
                        result='注册成功'
    else:
        result='账号密码不能为空'

    return render(request,'seller/register.html',locals())


@LoginValid
def index(request):
    Test.delay()
    return render(request,'seller/index.html')


def login(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    if email and password:
        flag=LoginUser.objects.filter(email=email,password=setPassword(password),user_type=0).first()
        if flag:
            response=HttpResponseRedirect('/seller/index')
            response.set_cookie('email',email)
            response.set_cookie('username',flag.username)
            response.set_cookie('user_id',flag.id)
            request.session['email']=email
            return response
        else:
            result='账号或密码错误'
    else:
        result='账号密码不能为空'
    return render(request,'seller/login.html',locals())


import hashlib
def setPassword(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result


def logout(request):
    response=HttpResponseRedirect('/login/')
    response.delete_cookie('email')
    del request.sisseon['email']
    return response

def base(request):

    return render(request,'seller/base.html')

@LoginValid
def goods_list(requset,type,page=1):
    user_id=requset.COOKIES.get('user_id')
    user=LoginUser.objects.get(id=int(user_id))

    goods = Goods.objects.filter(goods_status=int(type),goods_store=user).order_by('goods_number')
    goods_obj=Paginator(goods,10)
    goods_list=goods_obj.page(page)
    # return render(requset,'goodslistvue.html')
    return render(requset,'seller/goods_list.html',locals())

import random
def add_goods(request):
    goods_name="芹菜、西芹、菠菜、香菜、茼蒿、茴香、生菜、苋菜、莴苣、葱、香葱、分葱、胡葱、楼子葱、蒜头、洋葱头、韭菜、韭葱、黄瓜、丝瓜、冬瓜、菜瓜、苦瓜、南瓜、栉瓜、西葫芦、葫芦、瓠瓜、节瓜、越瓜、笋瓜、佛手瓜"
    address = "北京市，天津市，上海市，重庆市，河北省，山西省，辽宁省，吉林省，黑龙江省，江苏省，浙江省，安徽省，福建省，江西省，山东省，河南省，湖北省，湖南省，广东省，海南省，四川省，贵州省，云南省，陕西省，甘肃省，青海省，台湾省"
    goods_name=goods_name.split('、')
    address=address.split('，')
    for i,j in enumerate(range(100),1):
        goods=Goods()
        goods.goods_number=str(i).zfill(5)
        goods.goods_name=random.choice(address)+random.choice(goods_name)
        goods.goods_price=random.random()*100
        goods.goods_count=random.randint(1,100)
        goods.goods_location=random.choice(address)
        goods.goods_safe_data=random.randint(1,12)
        goods.save()

    return HttpResponse('增加数据')

def goods_status(request,type,id):
    goods = Goods.objects.filter(id=int(id)).first()
    if type == 'down':
        goods.goods_status=0
        goods.save()
    else:
        goods.goods_status=1
        goods.save()


    url=request.META.get("HTTP_REFERER")
    print(url)
    return HttpResponseRedirect(url)

@LoginValid
def PersonInfo(request):
    ## 查询用户的信息
    ## 登录的时候获取用户名 邮箱
    ## 查询
    user_id = request.COOKIES.get("user_id")
    user = LoginUser.objects.get(id = user_id)
    if request.method == "POST":
        print (request.POST)
        data = request.POST
        ## 更新数据
        user.username = data.get("username")
        user.phone_number = data.get("phone_number")
        user.age = data.get("age")
        user.gender = data.get("gender")
        user.address = data.get("address")
        # user.photo = data.get("photo")
        user.photo = request.FILES.get("photo")
        user.save()

    return render(request,"seller/personal_info.html",locals())




def goods_add(request):
    goods_type=GoodsType.objects.all()
    if request.method=='POST':
        user_id=request.COOKIES.get('user_id')
        goods=Goods()
        goods.goods_number=request.POST.get('goods_number')
        goods.goods_name=request.POST.get('goods_name')
        goods.goods_price=request.POST.get('goods_price')
        goods.goods_count=request.POST.get('goods_count')
        goods.goods_location=request.POST.get('goods_location')
        goods.goods_safe_data=request.POST.get('goods_safe_data')
        goods.goods_status=1
        goods.goods_type_id = int(request.POST.get("goods_type"))
        goods.goods_store_id=user_id
        goods.goods_picture =request.FILES.get("goodsfile")
        goods.save()

    return render(request, 'seller/goods_add.html',locals())

from sdk.sendDD import senddingding
import random
def get_code(request):
    result={'code':10000,'msg':''}
    code=random.randint(1000,9999)
    params={
        'content':'您的验证码为%s,不要告诉其他人' %code,
        'atMobiles':[],
        'isAtAll':True
    }
    try:
        senddingding(params)
        ValidCode.objects.create(code=code, user=request.GET.get("email"))
        result = {'code':10000, 'msg':'发送验证码成功'}
    except:
        result={'code':10001, 'msg':'发送验证码失败'}

    return JsonResponse(result)


def middletest(request,date):
    print('我是视图')

    def test():
        return HttpResponse('123455')
    rep=HttpResponse('middletest')
    rep.render=test
    return rep