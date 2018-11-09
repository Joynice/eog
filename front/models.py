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
    '''
    用户登录：用户名、密码、邮箱、真实姓名、加入时间、头像地址
    '''
    meta = {'collection': 'user'}
    _id = db.StringField(default=shortuuid.uuid)
    username = db.StringField(required=True, max_length=50)
    password = db.StringField(required=True, max_length=200)
    email = db.EmailField(required=True, max_length=100)
    realname = db.StringField(required=True, max_length=10)
    join_time = db.DateTimeField(required=False, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    avatar_path = db.StringField(required=False)

    def avatar(self):
        print(sep+'static'+sep+'eog'+sep+'img'+sep+'default'+sep+random.choice(os.listdir('./static/eog/img/default/')))
        return sep+'static'+sep+'eog'+sep+'img'+sep+'default'+sep+random.choice(os.listdir('./static/eog/img/default/'))
    # def __init__(self, *args, **kwargs):
    #     if 'password' in kwargs:
    #         self.password = kwargs.get('password')
    #         kwargs.pop('password')
    #     super(User, self).__init__(*args, **kwargs)
    #
    # @property
    # def password(self):
    #     return self.password1
    #
    # @password.setter
    # def password(self, newpwd):
    #     self.password1 = generate_password_hash(newpwd)
    #
    # def check_password(self, rawpwd):
    #     return check_password_hash(self.password1, rawpwd)


class Log(db.Document):
    '''
    用户日志： 登录时间，登出时间，登录ip
    todo:
    记录审核日志
    '''
    meta = {'collection': 'user_log'}
    _id = db.StringField(default=shortuuid.uuid)
    handler = db.StringField(required=True)
    ip = db.StringField(required=True)
    login_time = db.DateTimeField(required=False)
    logout_time = db.DateTimeField(required=False)
    today = db.DateTimeField(requried=False, default=datetime.datetime.now().strftime('%Y-%m-%d'))
