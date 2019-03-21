import xadmin
from .models import VerifyCode


class VerifyCodeXadmin(object):
    list_display = ['code', 'mobile', 'add_time']
    search_fields = ['code', 'mobile', 'add_time']
    list_filter = ['code', 'mobile', 'add_time']


xadmin.site.register(VerifyCode, VerifyCodeXadmin)
