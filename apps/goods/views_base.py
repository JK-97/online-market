from django.views.generic.base import View

from .models import Goods


class GoodsListView(View):
    def get(self, request):
        """
        通过django的view实现商品列表页
        :param request:
        :return:
        """
        json_list = []
        goods = Goods.objects.all()[:10]
        # for good in goods:
        #     good_dict = {}
        #     good_dict['name'] = good.name
        #     good_dict['category'] = good.category.name
        #     good_dict['market_price'] = good.market_price
        #     json_list.append(good_dict)

        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)
        #

        #datetime,image不能序列化
        import json
        from django.core import serializers
        json_data = serializers.serialize("json",goods)
        json_data = json.loads(json_data)
        from django.http import HttpResponse,JsonResponse

        # return HttpResponse(json.dumps(json_list), content_type="application/json")
        # return HttpResponse(json_data, content_type="application/json")
        return JsonResponse(json_data,safe=False)