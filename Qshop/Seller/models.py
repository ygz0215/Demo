from django.db import models
from django.db.models import Manager
# Create your models here.
GENDER_LIST=(
    (0,'女'),
    (1,'男')
)

class MyUser(Manager):

    def addUser(self,email,password):
        flag=LoginUser.objects.filter(email=email,password=password).exists()
        if not flag:
            user=LoginUser.objects.create(email=email,password=password)
            return user
        else:
            return flag

    def getUser(self):
        email=LoginUser.objects.filter(user_type=1).values('email')
        return email

    def getGoods(self,user_id):
        from Buyer.models import PayOrder,OrderInfo
        goods_name_list=[]
        payroder=PayOrder.objects.filter(order_user=LoginUser.objects.get(id=user_id),order_status=2).all()
        for one in payroder:
            order_info=one.orderinfo_set.all()
            for goods in order_info:
                goods_name=goods.goods
                goods_name_list.append(goods_name.goods_name)
        return goods_name_list


class LoginUser(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.IntegerField(null=True, blank=True ,choices=GENDER_LIST)
    photo =models.ImageField(upload_to="img", default="1.jpg")
    address = models.TextField()
    user_type=models.IntegerField(default=1)
    objects=MyUser()

    class Meta:
        db_table='loginuser'


class GoodsType(models.Model):
    type_lebal=models.CharField(max_length=32)
    type_description=models.TextField()
    type_picture=models.CharField(max_length=64)
    class Meta:
        db_table='goodstype'



class ValidCode(models.Model):
    code=models.CharField(max_length=32,verbose_name='验证码内容')
    user=models.CharField(max_length=32,verbose_name='用户')
    date=models.DateTimeField(auto_now=True,verbose_name='创建时间')
    class Meta:
        db_table='validcode'


class Goods(models.Model):
    goods_number =models.CharField(max_length=32,verbose_name="商品编号")
    goods_name =models.CharField(max_length=32,verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品价格")
    goods_count = models.IntegerField(verbose_name="数量")
    goods_location = models.TextField(verbose_name="生产地")
    goods_safe_data = models.IntegerField(verbose_name="保质期") ##
    goods_pro_time =models.DateField(auto_now=True,verbose_name="生产日期") ##生产日期
    goods_status=models.IntegerField(default=1) ##0下架 1上架
    goods_picture=models.ImageField(upload_to="img",default="img/1.jpg")
    goods_type=models.ForeignKey(to=GoodsType,on_delete=models.CASCADE)
    goods_store=models.ForeignKey(to=LoginUser,on_delete=models.CASCADE)
    goods_description=models.TextField(verbose_name='商品描述',default='goods')
    class Meta:
        db_table = "goods"

