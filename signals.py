# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from blinker import Namespace
from front.models import Log, Account
from flask import g
import datetime

namespace = Namespace()

login_signal = namespace.signal('login')
logout_signal = namespace.signal('logout')
account_signal = namespace.signal('account')



def login_log(sender, handler, ip, login_time):
    log = Log(handler=handler, login_time=login_time, ip=ip,
              logout_time=(datetime.datetime.now() + datetime.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
              today=datetime.datetime.now().strftime('%Y-%m-%d'))
    log.save()


def logout_log(sender, logout_time):
    try:
        g.user_log.logout_time = logout_time
        g.user_log.save()
    except:
        pass


def change_lcon(sender, operate_time, ip, operate_detail='修改了头像'):
    account = Account(operate_time=operate_time, operator=g.eog_user.email, ip=ip, operate_detail=operate_detail, today=datetime.datetime.today().date())
    account.save()

def change_username(sender, operate_time,ip,operate_datail):
    account = Account(operate_time=operate_time, operator=g.eog_user.email,ip=ip,operate_detail=operate_datail,today=datetime.datetime.today().date())

login_signal.connect(login_log)
logout_signal.connect(logout_log)
account_signal.connect(change_lcon)

