import random
from users.models import VerifyCode
from django.core.mail import send_mail
from MxShop.settings import EMAIL_FROM



def get_code(n=6,alpha=True):
    s = '' # 创建字符串变量,存储生成的验证码
    for i in range(n):  # 通过for循环控制验证码位数
        num = random.randint(0,9)  # 生成随机数字0-9
        if alpha: # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
            upper_alpha = chr(random.randint(65,90))
            lower_alpha = chr(random.randint(97,122))
            num = random.choice([num,upper_alpha,lower_alpha])
        s = s + str(num)
    return s

def send_email(mobile,send_type="register"):
    code = get_code()

    email_title = ''
    email_body = ''
    if send_type == "register":
        email_title = "注册验证码"
        email_body = "你的验证码为{0}".format(code)
        send_status = send_mail(subject=email_title,message=email_body,from_email=EMAIL_FROM,recipient_list=[mobile])
        return send_status,code

    elif send_type == "forget":
        email_title = "慕学在线网密码重置链接"
        email_body = "请点击下面的链接重置你的账号：http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM, recipient_list=[mobile])
        return send_status,code
    elif send_type == "update_email":
        email_title = "慕学在线网邮箱修改链验证码"
        email_body = "你的邮箱验证码为{0}".format(code)
        send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM, recipient_list=[mobile])
        return send_status,code

