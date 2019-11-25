from rest_framework import  serializers
from LoginUser.models import *

class GoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Goods
        fields = [
            "id",
            "goods_number",
            "goods_name",
            "goods_price",
            "goods_count",
            "goods_location",
            "goods_safe_data",
            "goods_pro_time",
            "goods_status",
        ]