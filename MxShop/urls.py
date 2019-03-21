"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from MxShop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, GoodsCategoryListViewSet, HotSearchWordsViewSet, BannerViewSet, \
    IndexGoodsViewSet
from trade.views import ShoppingCarViewSet, OrderViewSet, AlipayView
from user_operation.views import UserFavViewSet, LeaveMessageViewSet, UserAdressViewSet
from users.views import VerifyViewSet, UserViewSet
from django.views.generic import TemplateView

# from goods.views_base import GoodsListView


router = DefaultRouter()
# 配置goods的url
router.register('goods', GoodsListViewSet, base_name='goods')
# 配置goodscategory的url
router.register('categorys', GoodsCategoryListViewSet, base_name='categorys')
# 配置热搜词
router.register('hotsearchs', HotSearchWordsViewSet, base_name='hotsearchs')
# 配置发送验证码
router.register('codes', VerifyViewSet, base_name='codes')
# 配置USER
router.register('users', UserViewSet, base_name='users')
# 收藏
router.register('userfavs', UserFavViewSet, base_name='userfavs')
# 用户留言
router.register('messages', LeaveMessageViewSet, base_name='messages')
# 用户收货地址
router.register('address', UserAdressViewSet, base_name='address')
# 购物车
router.register('shopcarts', ShoppingCarViewSet, base_name='shopcarts')
# 订单相关
router.register('orders', OrderViewSet, base_name='orders')
# 轮播图注册
router.register('banners', BannerViewSet, base_name='banners')
# 获取新品
router.register('newgoods', GoodsListViewSet, base_name='newgoods')
# 获取主页商品类别栏
router.register('indexgoods', IndexGoodsViewSet, base_name='indexgoods')
# goods_list = GoodsListViewset.as_view({
#     'get': 'list'
# })

urlpatterns = [
    path(r'xadmin/', xadmin.site.urls),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    path(r'', include(router.urls)),
    # drf的cookies和session认证
    path(r'api-auth/', include('rest_framework.urls')),
    path(r'docs/', include_docs_urls(title="慕学生鲜")),
    # drf自带的token认证
    path(r'api-token-auth/', views.obtain_auth_token),
    # jwt-token认证
    path(r'login/', obtain_jwt_token),

    path(r'alipay/return/', AlipayView.as_view(), name='alipay'),

    path(r'index/', TemplateView.as_view(template_name="index.html"), name="index"),
    # 第三方登录
    path('', include('social_django.urls', namespace='social'))
]
