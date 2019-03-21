import time

from rest_framework import serializers

from goods.models import Goods
from goods.serializers import GoodsSerializer
from .models import ShoppingCar, OrderInfo, OrderGoods
from utils.alipay import AliPay
from MxShop.settings import private_key_path, ali_pub_key_path


class ShoppingCarDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCar
        fields = "__all__"


class ShoppingCarSerializer(serializers.Serializer):
    # serializer 继承自baseserialier，需要override方法
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    nums = serializers.IntegerField(min_value=1, help_text="数量", label="数量",
                                    error_messages={
                                        "required": "请选择购买数量",
                                        "min_value": "商品数量下不能小于1",

                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        # 添加购物车不只是创建新的，须在原有的基础上增加。所以需要复写create方法。
        user = self.context["request"].user
        nums = validated_data['nums']
        # 外建反序列化后，成一个对象
        goods = validated_data["goods"]

        existed = ShoppingCar.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCar.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderInfoDetialSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            # 沙箱里面的appid值
            appid="2016092800614944",
            # notify_url是异步的url
            app_notify_url="http://203.195.158.200:8000/alipay/return/",
            # 我们自己商户的密钥
            app_private_key_path=private_key_path,
            # 支付宝的公钥
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            # debug为true时使用沙箱的url。如果不是用正式环境的url
            debug=True,  # 默认False,
            return_url="http://203.195.158.200:8000/alipay/return/"
        )
        url = alipay.direct_pay(
            # 订单标题
            subject=obj.order_sn,
            # 我们商户自行生成的订单号
            out_trade_no=obj.order_sn,
            # 订单金额
            total_amount=obj.order_mount,
            # 成功付款后跳转到的页面，return_url同步的url
            return_url="http://203.195.158.200:8000/alipay/return/"
        )
        # 将生成的请求字符串拿到我们的url中进行拼接
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_sn = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            # 沙箱里面的appid值
            appid="2016092800614944",
            # notify_url是异步的url
            app_notify_url="http://203.195.158.200:8000/alipay/return/",
            # 我们自己商户的密钥
            app_private_key_path=private_key_path,
            # 支付宝的公钥
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            # debug为true时使用沙箱的url。如果不是用正式环境的url
            debug=True,  # 默认False,
            return_url="http://203.195.158.200:8000/alipay/return/"
        )
        url = alipay.direct_pay(
            # 订单标题
            subject=obj.order_sn,
            # 我们商户自行生成的订单号
            out_trade_no=obj.order_sn,
            # 订单金额
            total_amount=obj.order_mount,
            # 成功付款后跳转到的页面，return_url同步的url
            return_url="http://203.195.158.200:8000/alipay/return/"
        )
        # 将生成的请求字符串拿到我们的url中进行拼接
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    def generate_order_sn(self):
        # 当前时间+userid+随机数
        from random import Random
        random = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random.randint(10, 99))
        return order_sn

    class Meta:
        model = OrderInfo
        fields = "__all__"
