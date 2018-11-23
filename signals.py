# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from blinker import Namespace
from front.models import Log, Account
from flask import g
import datetime

namespace = Namespace()

login_signal = namespace.signal('login')
logout_signal = namespace.signal('logout')
change_lcon_signal = namespace.signal('change_lcon')
change_email_signal = namespace.signal('change_email')
change_password_signal = namespace.signal('change_password')
change_username_signal = namespace.signal('change_username')
forget_password_signal = namespace.signal('forget_password')


def login_log(sender, handler, ip, login_time):
    log = Log(handler=handler, login_time=login_time, ip=ip,
              logout_time=(datetime.datetime.now() + datetime.timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S"),
              today=datetime.datetime.now().strftime('%Y-%m-%d'))
    log.save()


def logout_log(sender, logout_time):
    try:
        g.user_log.logout_time = logout_time
        g.user_log.save()
    except:
        pass


def change_lcon(sender, operate_time, ip, operate_detail='修改头像'):
    account = Account(operate_time=operate_time, operator=g.eog_user.email, ip=ip, operate_detail=operate_detail,
                      today=datetime.datetime.today().date())
    account.save()


def change_username(sender, operate_time, ip, operate_detail='修改用户名'):
    account = Account(operate_time=operate_time, operator=g.eog_user.email, ip=ip, operate_detail=operate_detail,
                      today=datetime.datetime.today().date())
    account.save()


def change_email(sender, operate_time, ip, username, operate_detail='修改邮箱'):
    account = Account(operate_time=operate_time, operator=username, ip=ip, operate_detail=operate_detail,
                      today=datetime.datetime.today().date())
    account.save()


def change_password(sender, operate_time, ip, operate_detail='修改密码'):
    account = Account(operate_time=operate_time, operator=g.eog_user.email, ip=ip, operate_detail=operate_detail,
                      today=datetime.datetime.today().date())
    account.save()


def forget_password(sender, operate_time, ip, operator, operate_detail='重置密码'):
    account = Account(operate_time=operate_time, operator=operator, ip=ip, operate_detail=operate_detail,
                      today=datetime.datetime.today().date())
    account.save()


login_signal.connect(login_log)
logout_signal.connect(logout_log)
change_lcon_signal.connect(change_lcon)
change_username_signal.connect(change_username)
change_email_signal.connect(change_email)
change_password_signal.connect(change_password)
forget_password_signal.connect(forget_password)