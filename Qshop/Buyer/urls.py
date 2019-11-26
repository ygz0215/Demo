from django.urls import path,re_path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('index/',cache_page(200)(index)),
    path('login/',login),
    path('logout/',logout),
    path('register/',register),
    path('base/',base),
    path('goodslist/',goodslist),
    re_path('detail/(?P<goods_id>\d+)/',detail),
    path('user_center_info/',user_center_info),
    path('cart/',cart),
    path('place_order/',place_order),
    path('alipayorder/',alipayorder),
    path('payresult/',payresult),
    path('add_cart/',add_cart),
    path('del_cart/',del_cart),
    path('place_order_more/',place_order_more),
    path('user_center_order/',user_center_order),
    path('user_center_site/',user_center_site),
    path('test/',test),
]