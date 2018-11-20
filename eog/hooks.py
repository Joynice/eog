# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from .views import bp
import config
from flask import session, g, request
from front.models import User, Log, Account
from .models import Event_Search_Engine, Rule, Operate_Log
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
        account = Account.objects(operator=user.email,
                                  operate_time__gte=(datetime.datetime.now() - datetime.timedelta(days=7)).strftime(
                                      "%Y-%m-%d %H:%M:%S"),
                                  operate_time__lt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).order_by(
            '-operate_time').all()
        all_user = User.objects().all()
        if user:
            g.eog_user = user
            g.user_log = log
            g.all_log = all_today_log
            g.event_count = event_count
            g.rules_count = rules_count
            g.account = account
            g.all_user = all_user



@bp.after_request
def after_request(respones):
    '''
    记录登陆后的操作日志，可以将不想监控的操作加入到unpath中，监控路由对应的操作在config.py的xxx中进行添加或配置相应的说明
    例如，不想监控/xxx/ 路由
    对/xxx/l路由进行监控，并对其添加操作说明，‘审核ID:123事件为:误报’
    :param respones:
    :return:
    '''
    path = request.path
    ip = request.remote_addr
    ignore_path = ['/eog/events/', '/eog/rules/', '/eog/log/', '/eog/resetpwd/', '/eog/profile/', '/eog/my_log/',
                   '/eog/', '/eog/danger_event/', '/eog/review_event/',
                   '/eog/my_score/', '/eog/my_review/', '/eog/logout/', '/eog/account/', '/eog/resetmail/',
                   '/eog/resetusername/','/eog/source/']  # 不想被写进日志忽略的路由
    path_and_operation_detail = {'/eog/event_detail/': '查看安全事件{}详情'.format(request.form.get('event_id')),
                                 '/eog/event_suggestion/': '审核{id}事件为{status}'.format(id=request.form.get('id'),
                                                                                      status=request.form.get('status'))
                                 }  # 自定义添加被监测的日志详情说明
    if path in ignore_path:
        return respones
    if config.DevelopmentConfig.CMS_USER_ID in session:
        operate_log = Operate_Log(realname=g.eog_user.realname, ip=ip, path=path, today=datetime.datetime.today().date())
        if path in path_and_operation_detail.keys():
            operate_log.operation = path_and_operation_detail.get(path)
        operate_log.save()
        return respones
