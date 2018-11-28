# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from exts import db
import shortuuid
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
import random

sep = os.sep


class User(db.Document):
    """
    用户登录：用户名、密码、邮箱、真实姓名、加入时间、头像地址
    """
    meta = {'collection': 'user'}
    _id = db.StringField(default=shortuuid.uuid)
    username = db.StringField(required=True, max_length=50)
    password_hash = db.StringField(required=True)
    email = db.EmailField(required=True, max_length=100)
    realname = db.StringField(required=True, max_length=10)
    join_time = db.DateTimeField(required=False, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    avatar_path = db.StringField(required=False)

    # def __init__(self, *args, **kwargs):
    #     if 'password' in kwargs:
    #         print(111)
    #         self.password = kwargs.get('password')
    #         print(self.password)
    #         kwargs.pop('password')
    #     super(User, self).__init__(*args, **kwargs)
    #
    @property
    def password(self):
        raise AttributeError('password is not a readle attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self):
        print(sep + 'static' + sep + 'eog' + sep + 'img' + sep + 'default' + sep + random.choice(
            os.listdir('./static/eog/img/default/')))
        return sep + 'static' + sep + 'eog' + sep + 'img' + sep + 'default' + sep + random.choice(
            os.listdir('./static/eog/img/default/'))


class Log(db.Document):
    '''
    用户日志： 登录时间，登出时间，登录ip,登录日期
    todo:
    记录审核日志
    '''
    meta = {'collection': 'user_log'}
    _id = db.StringField(default=shortuuid.uuid)
    handler = db.StringField(required=True)
    ip = db.StringField(required=True)
    login_time = db.DateTimeField(required=False)
    logout_time = db.DateTimeField(required=False)
    today = db.DateTimeField(requried=False)


class Account(db.Document):
    """
    用户账号：操作时间、操作ip、具体操作、是否本人操作、操作日期
    """
    meta = {'collection': 'account'}
    _id = db.StringField(default=shortuuid.uuid)
    operator = db.StringField(required=False)
    ip = db.StringField(required=False)
    today = db.DateTimeField(required=False)
    operate_time = db.DateTimeField(required=False)
    operate_detail = db.StringField(required=False)
