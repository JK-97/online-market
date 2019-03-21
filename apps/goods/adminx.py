import xadmin
from .models import GoodsCategory, Goods, GoodsCategoryBrand, GoodsImage, Banner, HotSearchWords,IndexAd


class GoodsCategoryXadmin(object):
    list_display = ['name', 'category_type', 'parent_category', 'add_time']
    search_fields = ['name', 'category_type', 'parent_category']
    list_filter = ['name', 'category_type', 'parent_category']


class GoodsCategoryBrandXadmin(object):
    list_display = ['category','name', 'desc', 'add_time']
    search_fields = ['category','name', 'desc', 'add_time']
    list_filter = ['category','name', 'desc', 'add_time']


class GoodsXadmin(object):
    list_display = ['name', 'fav_num', 'goods_num', 'sold_num']
    search_fields = ['name', 'add_time']
    list_filter = ['name', 'fav_num', 'goods_num', 'sold_num']


class GoodsImageXadmin(object):
    list_display = ['goods', 'image_url', 'add_time']
    search_fields = ['goods', 'image_url', 'add_time']
    list_filter = ['goods', 'image_url', 'add_time']


class BannerXadmin(object):
    list_display = ['goods', 'index', 'add_time']
    search_fields = ['goods', 'index', 'add_time']
    list_filter = ['goods', 'index', 'add_time']


class HotSearchWordsXadmin(object):
    list_display = ['keywords', 'index', 'add_time']
    search_fields = ['keywords', 'index', 'add_time']
    list_filter = ['keywords', 'index', 'add_time']


class IndexAdXadmin(object):
    list_display = ['category', 'goods']
    search_fields = ['category', 'goods']
    list_filter =['category', 'goods']


xadmin.site.register(GoodsCategory, GoodsCategoryXadmin)
xadmin.site.register(GoodsCategoryBrand, GoodsCategoryBrandXadmin)
xadmin.site.register(Goods, GoodsXadmin)
xadmin.site.register(GoodsImage, GoodsImageXadmin)
xadmin.site.register(Banner, BannerXadmin)
xadmin.site.register(HotSearchWords, HotSearchWordsXadmin)
xadmin.site.register(IndexAd, IndexAdXadmin)
