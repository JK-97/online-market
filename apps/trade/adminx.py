import xadmin
from .models import ShoppingCar, OrderInfo, OrderGoods


class ShoppingCarXadmin(object):
    list_display = ['user', 'goods', 'nums']
    search_fields = ['user', 'goods', 'nums']
    list_filter = ['user', 'goods', 'nums']


class OrderInfoXadmin(object):
    list_display = ['user', 'order_sn', 'pay_status', 'post_script', 'order_mount', 'add_time']
    search_fields = ['user', 'order_sn', 'pay_status', 'post_script', 'order_mount', 'add_time']
    list_filter = ['user', 'order_sn', 'pay_status', 'post_script', 'order_mount', 'add_time']


class OrderGoodsXadmin(object):
    list_display = ['order', 'goods', 'goods_num', 'add_time']
    search_fields = ['order', 'goods', 'goods_num', 'add_time']
    list_filter = ['order', 'goods', 'goods_num', 'add_time']


xadmin.site.register(ShoppingCar, ShoppingCarXadmin)
xadmin.site.register(OrderInfo, OrderInfoXadmin)
xadmin.site.register(OrderGoods, OrderGoodsXadmin)
