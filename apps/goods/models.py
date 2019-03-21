from datetime import datetime
from django.db import models

from DjangoUeditor.models import UEditorField


# Create your models here.


class GoodsCategory(models.Model):
    """
    商品种类(name,code,desc,category_type,parent_category)
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    )
    name = models.CharField(default="", max_length=20, verbose_name="类别名", help_text="类别")
    code = models.CharField(default="", max_length=10, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", verbose_name="父类别", related_name="sub_cat", null=True, blank=True,
                                        on_delete=models.CASCADE)
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = "商品类别"

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    品牌(name,desc,image)
    """
    category = models.ForeignKey(GoodsCategory,on_delete=models.CASCADE,related_name='brands',null=True, blank=True, verbose_name="商品类目")
    name = models.CharField(default="", max_length=20, verbose_name="品牌名", help_text="品牌名")
    desc = models.TextField(default="", verbose_name="品牌描述", help_text="品牌描述")
    image = models.ImageField(max_length=200, upload_to="brands/")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "品牌"
        verbose_name_plural = "品牌"

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品(name,good_sn,good_brief,click_num,fav_num,sold_num,goods_num,shop_num,shop_free,is_new,good_desc,category)
    """
    name = models.CharField(max_length=30, verbose_name="品牌名", help_text="品牌名")
    good_sn = models.CharField(default="", max_length=20, verbose_name="商品唯一货号", help_text="商品唯一货号", blank=True,
                               null=True)
    goods_brief = models.CharField(default="", max_length=500, verbose_name="商品简介", help_text="商品简介", blank=True,
                                   null=True)
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    sold_num = models.IntegerField(default=0, verbose_name="商品销量")
    goods_num = models.IntegerField(default=0, verbose_name="库存数")
    market_price = models.IntegerField(default=0, verbose_name="市场价格")
    shop_price = models.IntegerField(default=0, verbose_name="本店价格")
    shop_free = models.BooleanField(default=False, verbose_name="是否承担邮费")
    is_new = models.BooleanField(default=False, verbose_name="是否新品")
    goods_desc = UEditorField(default="", verbose_name="品牌描述", help_text="品牌描述", imagePath="goods/images/",
                              filePath="goods/images/", width=1000, height=300, blank=True, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    goods_front_image = models.ImageField(upload_to="", default="", blank=True, null=True)
    category = models.ForeignKey(GoodsCategory, verbose_name="类别", on_delete=models.CASCADE)
    is_hot = models.BooleanField(default=False, verbose_name="是否热销")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """
    商品轮播图(goods,image,image_url)
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)
    image_url = models.CharField(max_length=300, verbose_name="图片路径", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品图片"
        verbose_name_plural = "商品图片"

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    轮播商品(goods,image,index)
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="banner", verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播商品"
        verbose_name_plural = "轮播商品"

    def __str__(self):
        return self.goods.name


class HotSearchWords(models.Model):
    keywords = models.CharField(max_length=5, verbose_name="热搜词", default="")
    index = models.IntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "热搜词"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords


class IndexAd(models.Model):
    """
    商品广告
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, related_name='category',verbose_name="商品类目")
    goods =models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='goods')

    class Meta:
        verbose_name = '首页广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name
