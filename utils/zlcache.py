# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from redis import Redis, StrictRedis
import config

cache = Redis(host=config.Config.REDIS_HOST, port=config.Config.REDIS_PORT,
              decode_responses=config.Config.REDIS_DECODE_RESPONSES,
              db=config.Config.REDIS_TASK_DB)

socket_cache = Redis(host=config.Config.REDIS_HOST, port=config.Config.REDIS_PORT,
                     decode_responses=config.Config.REDIS_DECODE_RESPONSES,
                     db=config.Config.REDIS_SOCKET_DB)


def set(key, value, timeout=120):
    return cache.set(key, value, timeout)


def get(key):
    return cache.get(key)


def delete(key):
    return cache.delete(key)


def socket_set(key, value):
    return socket_cache.set(key, value)


def socket_get(key):
    return socket_cache.get(key)


def socket_get_key():
    return socket_cache.keys()


def socket_get_keys():
    return socket_cache.keys()


