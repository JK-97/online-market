from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from goods.serializers import GoodsSerializer
from .models import UserFav, UserLeavingMessage, UserAddress


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ["goods", "id"]


class UserFavSerializer(serializers.ModelSerializer):
    # 获取当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        fields = ["user", "goods", "id"]
        validators = [
            # 此配置使用于在调用is_validate的判断条件，
            # 这里是lfields中的字段同时符合时才true，报错返回msg
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"

            )
        ]


class LeaveMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 这值只返回不提交
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "msg_type", "subject", "message", "file", "id", "add_time")


class UserAdressSerialzer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ("user", "province", "city", "district", "address", "signer_name", "signer_mobile", "id", "add_time")
