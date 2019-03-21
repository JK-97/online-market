from rest_framework import serializers
from django.db.models import Q
from .models import Goods, GoodsCategory, GoodsImage, HotSearchWords, Banner, GoodsCategoryBrand, IndexAd


class GoodsCategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializer2(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializer(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


class HotSearchWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class GoodsCategoryBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class IndexGoodsSerializer(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializer2(many=True)
    brands = GoodsCategoryBrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)[:3]
        if ad_goods:
            # 取到这个商品Queryset[0]
            good_ins = ad_goods[0].goods
            # 在serializer里面调用serializer的话，就要添加一个参数context（上下文request）,嵌套serializer必须加
            # serializer返回的时候一定要加 “.data” ，这样才是json数据
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    def get_goods(self, obj):
        catetory_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))[:6]
        goods_serializer = GoodsSerializer(catetory_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"
