# !/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'ChenTao'


from django_redis import get_redis_connection
from django.contrib.auth.models import User

redis = get_redis_connection()

KEY_CACHE_USER_TOKEN = 'key_cache_user:{username}_token'


def cache_set_user_token(user: User, token: str, expiration=60 * 60):
    key = KEY_CACHE_USER_TOKEN.format(username=user.username)
    if token:
        redis.set(key, token, expiration)


def cache_get_user_token(user):
    key = KEY_CACHE_USER_TOKEN.format(username=user.username)
    return redis.get(key)
