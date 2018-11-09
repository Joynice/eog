# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from blinker import Namespace
from front.models import Log
from flask import g
import datetime


namespace = Namespace()

login_signal = namespace.signal('login')
logout_signal = namespace.signal('logout')


def login_log(sender, handler, ip, login_time):
    log = Log(handler=handler, login_time=login_time, ip=ip, logout_time=(datetime.datetime.now()+datetime.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"))
    log.save()


def logout_log(sender, logout_time):
    print(g.eog_user.email)
    print(g.user_log.ip)
    g.user_log.logout_time = logout_time
    g.user_log.save()


login_signal.connect(login_log)
logout_signal.connect(logout_log)