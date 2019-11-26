from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from Seller.views import setPassword
from Seller.models import *
from .models import *
from django.db.models import Q

# Create your views here.

def LoginValid(func):
    def inner(request,*args,**kwargs):
        email=request.COOKIES.get('email')
        email_session=request.session.get('email')
        cookie_username=request.COOKIES.get('username')
        if email and email_session and email==email_session:
            flag=LoginUser.objects.filter(username=cookie_username,email=email,user_type=1).exists()
            if flag:
                return func(request,*args,**kwargs)
            else:
                return HttpResponseRedirect('/buyer/login')
        else:
            return HttpResponseRedirect('/buyer/login/')
    return inner

from django.views.decorators.cache import cache_page

# @LoginValid
cache_page(120)
def index(request):
    types=[]
    goods_type=GoodsType.objects.all()
    for one in goods_type:
        goods=one.goods_set.order_by('goods_price')
        if len(goods)>4:
            goods_all=goods[:4]
            types.append({'type':one,'goods':goods_all})
        elif len(goods)>0 and len(goods)<=4:
            goods_all=goods
            types.append({'type':one,'goods':goods_all})
    return render(request,'buyer/index.html',locals())

def login(request):
    email = request.POST.get('username')
    password = request.POST.get('pwd')
    if email and password:
        flag = LoginUser.objects.filter(email=email, password=setPassword(password),user_type=1).first()
        if flag:
            response = HttpResponseRedirect('/buyer/index')
            response.set_cookie('email', email)
            response.set_cookie('username', flag.username)
            response.set_cookie('user_id', flag.id)
            request.session['email'] = email
            return response
        else:
            result = '账号或密码错误'
    else:
        result = '账号密码不能为空'
    return render(request, 'buyer/login.html', locals())

def register(request):
    email = request.POST.get('email')
    password = request.POST.get('pwd')
    repassword = request.POST.get('cpwd')
    if email and password and repassword:
        if password != repassword:
            result = '密码不一致'
        else:
            flag = LoginUser.objects.filter(email=email).exists()
            if flag:
                result = '用户已存在'
            else:
                LoginUser.objects.create(email=email, username=email, password=setPassword(password),user_type=0)
                result = '注册成功'
    else:
        result = '账号密码不能为空'
    return render(request, 'buyer/register.html', locals())


def logout(request):
    response = HttpResponseRedirect('/buyer/login')
    response.delete_cookie('email')
    response.delete_cookie('username')
    response.delete_cookie('user_id')
    del request.session['email']
    return response


def base(request):

    return render(request,'buyer/base.html')

def goodslist(request):

    req_type = request.GET.get("req_type")
    keywords = request.GET.get("keywords")
     ## 查看指定类型的的商品
    if req_type == 'findall':
        goods_type = GoodsType.objects.get(id =int(keywords))
        goods_all = goods_type.goods_set.all()
        print(goods_all)
    ## 搜索 进行模糊查询
    else:
        goods_all =Goods.objects.filter(goods_name__icontains=keywords).all()
    ## 从搜索进来
    ## 进行模糊查询

    goods_new = goods_all.order_by("-goods_pro_time")[:2]
    return render(request,"buyer/goodslist.html",locals())

def detail(request,goods_id):
    goods=Goods.objects.get(id=int(goods_id))
    return render(request,'buyer/detail.html',locals())


def user_center_info(request):
    username=request.COOKIES.get('email')
    user=LoginUser.objects.filter(email=username).first()
    return render(request,'buyer/user_center_info.html',locals())

@LoginValid
def cart(request):

    user_id = request.COOKIES.get("user_id")
    order_number=PayOrder.objects.filter(order_user=LoginUser.objects.get(id=user_id),order_status=1).values('order_number')
    print(order_number)

    ## 查找用户的购物车内容， 按照时间逆序


    cart1=Cart.objects.filter(Q(payorder__in=order_number)|Q(payorder='1')).all().order_by('-id')

    return render(request,'buyer/cart.html',locals())

def user_center_order(request):
    user_id=request.COOKIES.get('user_id')
    payorder=PayOrder.objects.filter(order_user=LoginUser.objects.get(id=user_id)).all().order_by('order_status')
    return render(request,'buyer/user_center_order.html',locals())


def user_center_site(request):
    email=request.COOKIES.get('email')
    user=LoginUser.objects.filter(email=email).first()
    return render(request,'buyer/user_center_site.html',locals())

import time
def place_order(request):
    user_id=request.COOKIES.get('user_id')
    goods_id=request.GET.get('goods_id')
    goods_count=request.GET.get('goods_count')
    goods=Goods.objects.get(id=int(goods_id))
    payorder=PayOrder()
    payorder.order_number=str(time.time()).replace('.','')
    payorder.order_status='1'
    payorder.order_total=goods.goods_price * int(goods_count)
    payorder.order_user=LoginUser.objects.get(id=int(user_id))
    payorder.save()

    orderinfo = OrderInfo()
    orderinfo.order_id = payorder
    orderinfo.goods = goods
    orderinfo.goods_price = goods.goods_price
    orderinfo.goods_count = int(goods_count)
    orderinfo.goods_total_price = goods.goods_price * int(goods_count)
    orderinfo.save()
    return render(request,'buyer/place_order.html',locals())

from Qshop.settings import alipay

def alipayorder(request):
    order_id=request.GET.get('order_id')
    payorder = PayOrder.objects.get(id=order_id)
    order_string = alipay.api_alipay_trade_page_pay(
        subject='生鲜交易',  ## 交易主题
        out_trade_no=payorder.order_number,  ## 订单号
        total_amount=str(payorder.order_total),  ## 交易总金额  需要是一个string
        return_url='http://127.0.0.1:8000/buyer/payresult/',  ## 返回的路径
        notify_url=None
    )
    result = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return HttpResponseRedirect(result)



def payresult(request):
    out_trade_no=request.GET.get('out_trade_no')
    payorder=PayOrder.objects.get(order_number=out_trade_no)
    payorder.order_status=2
    payorder.save()
    return render(request,'buyer/payresult.html',locals())



def add_cart(request):
    goods_id=request.POST.get('goods_id')
    count=request.POST.get('count',1)
    user_id=request.COOKIES.get('user_id')
    goods=Goods.objects.get(id=goods_id)
    user=LoginUser.objects.get(id=user_id)
    has_cart=Cart.objects.filter(goods=goods,cart_user=user,payorder='1').first()
    if has_cart:
        has_cart.goods_number+= int(count)
        has_cart.goods_tatal+=int(count)*goods.goods_price
        has_cart.save()
    else:
        cart=Cart()
        cart.goods=goods
        cart.goods_number=int(count)
        cart.cart_user=LoginUser.objects.get(id=user_id)
        cart.goods_total=int(count) * goods.goods_price
        cart.save()

    return JsonResponse({'code':10000,'msg':'添加购物成功'})



def place_order_more(request):
    user_id=request.COOKIES.get('user_id')
    data=request.POST
    data=data.items()
    res=[]
    for k,v in data:
        if k.startswith('cartid'):
            res.append(v)
    user=LoginUser.objects.get(id=user_id)
    print(res)
    if len(res)!=0:
        payorder = PayOrder()
        payorder.order_number =str(time.time()).replace(".", "")
        payorder.order_status = 1  ## 未支付
        payorder.order_total = 0
        payorder.order_user = user
        payorder.save()

        order_total = 0
        order_count = 0
        for c_id in res:  ## c_id 购物车id
            cart = Cart.objects.get(id=c_id)
            goods = cart.goods
            orderinfo = OrderInfo()
            orderinfo.order_id = payorder
            orderinfo.goods = goods
            orderinfo.goods_price = goods.goods_price
            orderinfo.goods_count = cart.goods_number
            orderinfo.goods_total_price = cart.goods_total
            orderinfo.save()
            order_total += cart.goods_total
            order_count += cart.goods_number

            cart.payorder=payorder.order_number
            cart.save()
        payorder.order_total = order_total
        payorder.save()
    return render(request,'buyer/place_order.html',locals())




def del_cart(request):
    cart_id=request.GET.get('cart_id')
    Cart.objects.filter(id=cart_id).delete()
    return HttpResponseRedirect('/buyer/cart')


def test(request):

    return render(request,'buyer/test.html')



