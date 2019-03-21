from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import authentication
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from utils.email_send import send_email
from .models import VerifyCode
from .serializers import VerifySerializer, UserRegSerializer, UserDetailSerializer

# Create your views here.
User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户登录验证
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class VerifyViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送邮箱验证
    """
    serializer_class = VerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile"]
        send_status, code = send_email(mobile=mobile)
        if send_status:
            code_record = VerifyCode(code=code, mobile=mobile, add_time=datetime.now())
            code_record.save()

            return Response({
                "mobile": "发送成功"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "mobile": "发送失败"
            }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(mixins.RetrieveModelMixin,mixins.UpdateModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)

    # permission_classes = (permissions.IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        # 动态获取permissions
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer

    def get_permissions(self):
        # 动态获取permissions
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
