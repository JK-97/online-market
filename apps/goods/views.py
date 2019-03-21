# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import JSONParser
# from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .filters import GoodsFilter
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from .models import Goods, GoodsCategory, HotSearchWords, Banner
from .serializers import GoodsSerializer, GoodsCategorySerializer, HotSearchWordsSerializer, BannerSerializer, \
    IndexGoodsSerializer


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页,分页,搜索,排序
    """
    throttle_classes = (UserRateThrottle,AnonRateThrottle)
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filterset_fields = ('name', 'market_price')
    # 这样的过滤功能不多，不灵活
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_desc', 'goods_brief')
    ordering_fields = ('shop_price', 'add_time')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GoodsCategoryListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list：
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer


class HotSearchWordsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    热搜词
    """
    queryset = HotSearchWords.objects.all()[:5]
    serializer_class = HotSearchWordsSerializer


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list：获取轮播图
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexGoodsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取主页分类列表
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexGoodsSerializer
