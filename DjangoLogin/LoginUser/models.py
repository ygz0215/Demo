from django.db import models

# Create your models here.
GENDER_LIST=(
    (0,'女'),
    (1,'男')
)

class LoginUser(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.IntegerField(null=True, blank=True ,choices=GENDER_LIST)
    photo =models.ImageField(upload_to="img", default="1.jpg")
    address = models.TextField()

    class Meta:
        db_table='loginuser'


class Goods(models.Model):
    goods_number =models.CharField(max_length=32,verbose_name="商品编号")
    goods_name =models.CharField(max_length=32,verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品价格")
    goods_count = models.IntegerField(verbose_name="数量")
    goods_location = models.TextField(verbose_name="生产地")
    goods_safe_data = models.IntegerField(verbose_name="保质期") ##
    goods_pro_time =models.DateField(auto_now=True,verbose_name="生产日期") ##生产日期
    goods_status=models.IntegerField(default=1) ##0下架 1上架
    class Meta:
        db_table = "goods"