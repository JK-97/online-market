from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.alipay import AliPay
from datetime import datetime
from django.shortcuts import redirect
from rest_framework.response import Response
from MxShop.settings import ali_pub_key_path, private_key_path
from utils.permissions import IsOwnerOrReadOnly
from .models import ShoppingCar, OrderInfo, OrderGoods
from .serializers import ShoppingCarSerializer, ShoppingCarDetailSerializer, OrderInfoSerializer, \
    OrderInfoDetialSerializer
from django.contrib.auth import get_user_model


# Create your views here.


class ShoppingCarViewSet(viewsets.ModelViewSet):
    """
    list:
        获取购物车列表
    destroy:
        清空购物车
    create:
        加入购物车
    update:
        修改购物车
    """
    serializer_class = ShoppingCarSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCarDetailSerializer
        else:
            return ShoppingCarSerializer

    def get_queryset(self):
        return ShoppingCar.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        shop_car = serializer.save()
        goods = shop_car.goods
        goods.goods_num -= shop_car.nums
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = ShoppingCar.objects.get(id=serializer.instance.id)
        existed_num = existed_record.nums
        save_record = serializer.save()
        nums = save_record.nums - existed_num
        goods = save_record.goods
        goods.goods_num += nums
        goods.save()


class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    订单管理
    list:
        获取订单列表
    destroy:
        清空订单
    create:
        增加订单

    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderInfoSerializer
        elif self.action == "retrieve":
            return OrderInfoDetialSerializer
        return OrderInfoSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCar.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order


from rest_framework.views import APIView


class AlipayView(APIView):
    def get(self, request):
        """
        处理支付宝的return_url返回
        """
        processed_dict = {}
        # 1. 获取GET中参数
        for key, value in request.GET.items():
            processed_dict[key] = value
        # 2. 取出sign
        sign = processed_dict.pop("sign", None)

        # 3. 生成ALipay对象
        alipay = AliPay(
            appid="2016092800614944",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/",
        )

        verify_re = alipay.verify(processed_dict, sign)

        # 这里可以不做操作。因为不管发不发return url。notify url都会修改订单状态。
        if verify_re is True:
            # order_no = processed_dict.get('out_trade_no', None)
            # trade_no = processed_dict.get('trade_no', None)
            # trade_status = processed_dict.get('trade_status', None)
            #
            # existed_orders = OrderInfo.objects.filter(order_sn=order_no)
            # for existed_order in existed_orders:
            #     existed_order.pay_status = trade_status
            #     existed_order.trade_sn = trade_no
            #     existed_order.order_sn = order_no
            #     existed_order.pay_time = datetime.now()
            #     existed_order.save()

            response = redirect("/index/#/app/home/member/order")
            # response.set_cookie("nextPath","pay",max_age=5)
            # 跳转到都将哦代理的index界面，设置cookies，再前端跳转
            return response

        else:
            response = redirect("index")
            return response

    def post(self, request):
        """
        处理支付宝的notify_url
        """
        # 存放post里面所有的数据
        processed_dict = {}
        # 取出post里面的数据
        for key, value in request.POST.items():
            processed_dict[key] = value
        # 把signpop掉，文档有说明
        sign = processed_dict.pop("sign", None)

        # 生成一个Alipay对象
        alipay = AliPay(
            appid="2016091500517456",
            app_notify_url="http://47.93.198.159:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.93.198.159:8000/alipay/return/"
        )

        # 进行验证
        verify_re = alipay.verify(processed_dict, sign)

        # 如果验签成功
        if verify_re is True:
            # 商户网站唯一订单号
            order_no = processed_dict.get('out_trade_no', None)
            # 支付宝系统交易流水号
            trade_no = processed_dict.get('trade_no', None)
            # 交易状态
            trade_status = processed_dict.get('trade_status', None)

            # 查询数据库中订单记录
            existed_orders = OrderInfo.objects.filter(order_sn=order_no)
            for existed_order in existed_orders:
                # 订单商品项
                order_goods = existed_order.goods.all()
                # 商品销量增加订单中数值
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                # 更新订单状态
                existed_order.pay_status = trade_status
                existed_order.order_sn = order_no
                existed_order.trade_sn = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            # 需要返回一个'success'给支付宝，如果不返回，支付宝会一直发送订单支付成功的消息
            return Response("success")
