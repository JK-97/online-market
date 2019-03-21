from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models

from goods.models import Goods

# Create your models here.
User = get_user_model()


class ShoppingCar(models.Model):
    """
    购物车(user,goods,nums)
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    nums = models.IntegerField(default=0, verbose_name="购买数量")

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return "%s(%d)".format(self.goods.name, self.user.nums)


class OrderInfo(models.Model):
    """
    定单信息(user,order_sn,trade_sn,pay_status,post_script,order_mount,pay_time,address,signer)
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED","交易结束"),
        ("paying","待支付")
    )

    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    order_sn = models.CharField(verbose_name="定单号",null=True,blank=True,max_length=100)
    trade_sn = models.CharField(verbose_name="交易流水号", unique=True,null=True,blank=True,max_length=50)
    pay_status = models.CharField(choices=ORDER_STATUS, default="paying",verbose_name="订单状态", max_length=60)
    post_script = models.CharField(default="", max_length=100, verbose_name="订单留言", null=True, blank=True)
    order_mount = models.CharField(default=0.0, verbose_name="订单金额", max_length=100)
    pay_time = models.DateTimeField(default=datetime.now, verbose_name="支付时间")
    # 用户信息
    address = models.CharField(default="", max_length=100, verbose_name="收获地址")
    singer_mobile=models.CharField(default="", max_length=50, verbose_name="签收人电话")
    signer_name = models.CharField(default="", max_length=20, verbose_name="签收人")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "定单信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    """
    定单的商品详情(order,goods,goods_num)
    """
    order = models.ForeignKey(OrderInfo, verbose_name="定单", on_delete=models.CASCADE,related_name="goods")
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    goods_num = models.IntegerField(default=0, verbose_name="购买数量")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "定单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
