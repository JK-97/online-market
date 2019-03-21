import re
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework import serializers
import pytz
from .models import VerifyCode
from rest_framework.validators import UniqueValidator
REGEX_EMAIL = "^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
User = get_user_model()


class VerifySerializer(serializers.ModelSerializer):
    """
    验证邮箱好吗
    """
    mobile = serializers.CharField(max_length=30)

    def validate_mobile(self, mobile):
        """
        邮箱验证号码
        :param mobile:
        :return:
        """
        # 邮箱是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已存在")

        # 验证邮箱是否合法
        if not re.match(REGEX_EMAIL, mobile):
            raise serializers.ValidationError("邮箱非法")

        # 验证发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile):
            raise serializers.ValidationError("距离上一次发送为未超过60s")

        return mobile

    class Meta:
        model = VerifyCode
        fields = ["mobile"]


class UserRegSerializer(serializers.ModelSerializer):
    # 这是serializers的基础验证，验证code的长度
    password = serializers.CharField(write_only=True,label="密码",style={'input_type':'password'})
    code = serializers.CharField(write_only=True,max_length=10, min_length=4,help_text="验证码",label="验证码",error_messages={
        "required":"请输入验证码",
        "blank":"请输入验证码",
        "max_length":"验证码格式错误",
        "min_length": "验证码格式错误",
    })
    username = serializers.CharField(required=True,allow_blank=False,validators=[UniqueValidator(queryset=User.objects.all(),message="用户已存在")])
    def validate_code(self, code):
        # 单独验证code的fields，功能比form强大很多
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            five_minutes_ago = datetime.now().replace(tzinfo=pytz.timezone('UTC')) - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError("验证吗过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")
    # def create(self, validated_data):
    #     user =super(UserRegSerializer,self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user
    def validate(self, attrs):
        # validate是所有fields验证后返回的值
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile","password")
#配置readonly后不会进行序列化


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """
    class Meta:
        model = User
        fields = ("name","gender","birthday","email","mobile")