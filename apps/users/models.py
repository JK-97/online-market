from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class UserProfile(AbstractUser):
    """
    用户(name,mobile,birthday,email,gender)
    需要在setting中替换系统用户
    AUTH_USER_MODEL = 'users.UserProfile'
    """
    name = models.CharField(max_length=30, verbose_name="姓名", blank=True, null=True)
    mobile = models.CharField(max_length=50, verbose_name='手机号码',blank=True,null=True)
    birthday = models.DateField(max_length=10, verbose_name="生日", blank=True, null=True)
    email = models.CharField(max_length=30, verbose_name="邮件", blank=True, null=True)
    gender = models.CharField(max_length=10, verbose_name="性别", choices=(("male", "女"), ("female", "男")),
                              default="male", blank=True, null=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return str(self.username)


class VerifyCode(models.Model):
    """
    短信验证码(code,mobile)
    """
    code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=50, verbose_name='邮箱')
    add_time = models.DateTimeField(max_length=20, verbose_name="添加时间")

    class Meta:
        verbose_name = "验证码"
        verbose_name_plural = " 验证码"

    def __str__(self):
        return self.code
