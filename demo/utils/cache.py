# !/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'ChenTao'


from django_redis import get_redis_connection
from django.contrib.auth.models import User

redis = get_redis_connection()

KEY_CACHE_USER_TOKEN = 'key_cache_user:{username}_token'


def _user_token(user):
    """
    保存token的key值，主要需要User的username属性
    """
    return KEY_CACHE_USER_TOKEN.format(username=user.username)


def cache_set_user_token(user: User, token: str, expiration=60 * 60):
    """
    将用户每次登录的token值加入缓存中，每个用户的这个值只存在一次
    :param user: User对象
    :param token: token值
    :param expiration: 过期时间
    """
    key = _user_token(user)
    if token:
        redis.set(key, token, expiration)


def cache_get_user_token(user):
    """
    返回保存在缓存中的token值
    :param user: User对象
    :return: 保存的token值
    """
    key = _user_token(user)
    return redis.get(key)
