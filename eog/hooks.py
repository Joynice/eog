# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from .views import bp
import config
from flask import session, g
from front.models import User, Log
from .models import Event_Search_Engine, Rule
import datetime


@bp.before_request
def before_request():
    if config.DevelopmentConfig.CMS_USER_ID in session:
        user_id = session.get(config.DevelopmentConfig.CMS_USER_ID)
        user = User.objects(_id=user_id).first()
        event_count = Event_Search_Engine.objects().count()
        rules_count = Rule.objects().count()
        log = Log.objects(handler=user.email).order_by('-login_time').first()
        all_today_log = Log.objects(handler=user.email,
                                    today=str(datetime.datetime.now().strftime('%Y-%m-%d')) + ' ' + '0:00:00').order_by(
            '-login_time').all()
        if user:
            g.eog_user = user
            g.user_log = log
            g.all_log = all_today_log
            g.event_count = event_count
            g.rules_count = rules_count
