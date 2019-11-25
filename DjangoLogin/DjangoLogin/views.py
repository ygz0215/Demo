from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from LoginUser.models import *
from django.core.paginator import Paginator
from django.views import View
import json


def LoginValid(func):
    def inner(request,*args,**kwargs):
        email=request.COOKIES.get('email')
        email_session=request.session.get('email')
        if email and email_session and email==email_session:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return inner



def register(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    repassword=request.POST.get('repassword')
    if email and password and repassword:
        if password != repassword:
            result='密码不一致'
        else:
            flag = LoginUser.objects.filter(email=email).exists()
            if flag:
                result='用户已存在'
            else:
                LoginUser.objects.create(email=email,username=email,password=setPassword(password))
                result='注册成功'

    else:
        result='账号密码不能为空'

    return render(request,'register.html',locals())


@LoginValid
def index(request):

    return render(request,'index.html')

def login(request):
    print('111')
    email=request.POST.get('email')
    password=request.POST.get('password')
    if email and password:
        flag=LoginUser.objects.filter(email=email,password=setPassword(password)).first()
        if flag:
            response=HttpResponseRedirect('/index')
            response.set_cookie('email',email)
            response.set_cookie('username',flag.username)
            response.set_cookie('user_id',flag.id)
            request.session['email']=email
            return response
        else:
            result='账号或密码错误'
    else:
        result='账号密码不能为空'
    return render(request,'login.html',locals())


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

    return render(request,'base.html')

def goods_list(requset,type,page=1):
    goods = Goods.objects.filter(goods_status=int(type)).order_by('goods_number')
    goods_obj=Paginator(goods,10)
    goods_list=goods_obj.page(page)
    # return render(requset,'goodslistvue.html')
    return render(requset,'goods_list.html',locals())

def vuedemo(requset):

    return render(requset,'vuedemo.html')

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



def goods_list_api(request,type,page=1):
    """
    type  ->   0  获取  下架的商品
                1   获取上架的商品
    :param request:
    :param type:
    :param page:
    :return:
    """
    print (type)
    ## 查询   返回数据
    # goods = Goods.objects.all().order_by("-goods_number")
    goods = Goods.objects.filter(goods_status = int(type)).order_by("-goods_number")
    ##
    goods_obj = Paginator(goods,10)  ## 每页10条
    goods_list = goods_obj.page(page)
    # return render(request,'goods_list.html',locals())
    res = []
    for one in goods_list:
        res.append({
            "goods_number":one.goods_number,
            "goods_name":one.goods_name,
            "goods_price":one.goods_price,
            "goods_count":one.goods_count,
            "goods_location":one.goods_location,
            "goods_safe_data":one.goods_safe_data,
            "goods_pro_time":one.goods_pro_time,
            "goods_status":one.goods_status,
        })



    result = {
        "page_range":list(goods_obj.page_range),
        "data":res,
        "page":page,
    }
    return JsonResponse(result)


class GoodsView(View):
    def __init__(self):
        super(GoodsView, self).__init__()
        self.result={
            'methods':'get',
            'data':'',
            'version':'v1.0'
        }

    def get(self,request):
        id=request.GET.get('id')
        if id:
            goods=Goods.objects.get(id=id)
            data={
                "goods_number": goods.goods_number,
                "goods_name": goods.goods_name,
                "goods_price": goods.goods_price,
                "goods_count": goods.goods_count,
                "goods_location": goods.goods_location,
                "godds_safe_data":goods.goods_safe_data,
                "goods_pro_time": goods.goods_pro_time,
                "goods_status": goods.goods_status,
            }
        else:
            goods=Goods.objects.all()
            data=[]
            for one in goods:
                data.append({
                    "goods_number": one.goods_number,
                    "goods_name": one.goods_name,
                    "goods_price": one.goods_price,
                    "goods_count": one.goods_count,
                    "goods_location": one.goods_location,
                    "godds_safe_data": one.goods_safe_data,
                    "goods_pro_time": one.goods_pro_time,
                    "goods_status": one.goods_status,
                })
        self.result={'methods':'get',
                     'data':data,
                     }
        return JsonResponse(self.result)

    def post(self,request):
        data=request.POST
        goods=Goods()
        goods.goods_number=data.get('goods_number')
        goods.goods_name=data.get('goods_name')
        goods.goods_price=data.get('goods_pirce')
        goods.goods_count=data.get('goods_count')
        goods.goods_location=data.get('goods_location')
        goods.goods_number=data.get('goods_number')
        goods.save()
        self.result['methods']= "post"
        self.result['data']= {id:goods.id}
        self.result['msg']= "数据添加成功"
        return JsonResponse(self.result)


    def put(self, request):

        ## 获取数据 进行更新
        # data = request.POST put 请求的数据，不在request.GET或者POST中
        data = request.body  ## bytes 类型
        data = json.loads(data.decode())
        id = data.get("id")
        goods_name = data.get("goods_name")
        ## 更新 操作 将指定id的商品名字修改
        Goods.objects.filter(id=id).update(goods_name=goods_name)
        self.result = {"methods": "put请求"}
        self.result["data"] = {"id": id}
        self.result["msg"] = "数据修改完成"
        return JsonResponse(self.result)

    def delete(self, request):
        data = request.body

        data = json.loads(data.decode())
        id = data.get("id")
        ## 删除
        Goods.objects.filter(id=id).delete()
        self.result = {"methods": "delete请求"}
        self.result["data"] = {"id": id}
        self.result["msg"] = "数据删除完成"
        return JsonResponse(self.result)



from rest_framework import viewsets
from .serializer import GoodSerializer
class GoodsViewsSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodSerializer


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

    return render(request,"personal_info.html",locals())