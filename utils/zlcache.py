# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from redis import Redis
import config


cache = Redis(host=config.Config.REDIS_HOST, port=config.Config.REDIS_PORT, decode_responses=config.Config.REDIS_DECODE_RESPONSES,
              db=config.Config.REDIS_TASK_DB)

def set(key, value, timeout=120):
    return cache.set(key, value, timeout)


def get(key):
    return cache.get(key)


def delete(key):
    return cache.delete(key)
