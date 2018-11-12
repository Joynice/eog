# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from flask import session, redirect, url_for, g
from functools import wraps
import config


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if config.DevelopmentConfig.CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('front.login'))
    return inner