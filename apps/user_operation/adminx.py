import xadmin
from .models import UserFav, UserAddress, UserLeavingMessage


class UserFavXadmin(object):
    list_display = ['user', 'goods']
    search_fields = ['user', 'goods']
    list_filter = ['user', 'goods']


class UserAddressXadmin(object):
    list_display = ['user', 'address', 'signer_name', 'signer_mobile']
    search_fields = ['user', 'address', 'signer_name', 'signer_mobile']
    list_filter = ['user', 'address', 'signer_name', 'signer_mobile']


class UserLeavingMessageXadmin(object):
    list_display = ['user', 'msg_type', 'subject', 'message']
    search_fields = ['user', 'msg_type', 'subject', 'message']
    list_filter = ['user', 'msg_type', 'subject', 'message']


xadmin.site.register(UserFav, UserFavXadmin)
xadmin.site.register(UserAddress, UserAddressXadmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageXadmin)
