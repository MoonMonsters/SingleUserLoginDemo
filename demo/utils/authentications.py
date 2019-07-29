# !/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'ChenTao'

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import exceptions

from demo.utils.cache import cache_get_user_token


class UserTokenAuthentication(JSONWebTokenAuthentication):

    def authenticate(self, request):
        # 获取返回值(user, token)
        user_auth_tuple = super().authenticate(request)

        # 如果返回值为空，则说明验证失败
        if not user_auth_tuple or not user_auth_tuple[0] or not user_auth_tuple[1]:
            raise exceptions.AuthenticationFailed('帐号或密码错误')

        # 缓存的用户token
        token = cache_get_user_token(user_auth_tuple[0])
        # 如果当前登录用户的token和访问携带的token不一致，就说明此次访问的token已失效
        if token != user_auth_tuple[1]:
            raise exceptions.AuthenticationFailed('帐号已在其他地方登录!')

        # 否则继续往下执行
        return user_auth_tuple
