# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from flask import Blueprint, render_template, request, redirect, flash, url_for, session, views, g, jsonify
from utils.mongo import insert_rules, find_rules, count_rule, find_one_rules, delete_rule, SecEvent
import time
from config import Config, DevelopmentConfig
from flask_paginate import Pagination, get_page_args, get_page_parameter
from .models import Event_Search_Engine, Rule, Operate_Log
from .decorators import login_required
from .forms import ResetEmailForm, ResetpwdForm, ResetUsernameForm, AddSuggesionEvent
from utils import restful
from front.models import User, Log, Account
import os
from signals import logout_signal, change_email_signal, change_password_signal, change_username_signal, \
    change_lcon_signal
from datetime import datetime

bp = Blueprint('eog', __name__, url_prefix='/eog')
secE_db = SecEvent()
timeStruct = time.localtime(time.time())
strTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeStruct)
ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg', 'gif']


@bp.route('/')
@login_required
def index():
    return render_template('eog/today_event.html')


@bp.route('/test/')
@login_required
def test():
    return render_template('eog/test.html')


@bp.route('/rule/', methods=['GET', 'POST'])
@login_required
def rule():
    if request.method == 'GET':
        rules_count = Rule.objects().count()
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page - 1) * Config.RULE_PER_PAGE
        end = start + Config.RULE_PER_PAGE
        pagination = Pagination(bs_version=3, page=page, total=rules_count, per_page=Config.PER_PAGE)
        rules = Rule.objects()[start:end]
        if rules:
            flash("规则库中共有{}条规则".format(rules_count))
        else:
            flash("查询错误，请检查后再次查询")
        context = {
            "rules": rules,
            "pagination": pagination
        }
        return render_template('eog/rule.html', **context)
    else:
        req = request.form
        rule = req.get("rule")
        type = req.get("type")
        leave = req.get("leave")
        des = req.get("des")
        suggestion = req.get("suggestion")
        if Rule.objects(rule=rule).first():
            flash("插入数据已存在，请检查后重试")
            return redirect(url_for('rule'))
        rule = Rule(rule=rule, type=type, leave=leave, des=des, suggestion=suggestion)
        rule.save()
        flash("插入数据成功")
        return redirect(url_for('rule'))


@bp.route('/delete/', methods=["POST"])
@login_required
def delete():
    if request.method == "POST":
        form = request.form
        print(form)
        del_rule = form.get('delete')
        print(del_rule)
        if delete_rule(del_rule) is 1:
            flash("删除数据成功")
            return redirect(url_for('rule'))
        else:
            flash("删除数据失败")
            return redirect(url_for('rule'))


@bp.route('/today_event/')
@login_required
def today_event():
    return render_template('eog/today_event.html')


@bp.route('/events/')
@login_required
def events():
    if request.method == 'GET':
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page - 1) * Config.EVENT_PER_PAGE
        end = start + Config.EVENT_PER_PAGE
        event_count = Event_Search_Engine.objects().count()
        pagination = Pagination(bs_version=3, page=page, total=event_count, per_page=Config.EVENT_PER_PAGE)
        event_abstract = (Event_Search_Engine.objects)[start:end]

        context = {
            "event_abstract": event_abstract,
            "pagination": pagination,
            "event_count": event_count,
        }
        return render_template('eog/events.html', **context)


@bp.route('/event_detail/', methods=['POST'])
@login_required
def event_detail():
    event_id = request.form.get('event_id')
    event_abstract = (Event_Search_Engine.objects(_id=event_id).first())
    img_base64 = (event_abstract["img"][2:-1])
    return jsonify({"data": event_abstract, "img": img_base64})


@bp.route('/event_suggestion/', methods=['POST'])
def event_suggestion():
    form = AddSuggesionEvent(request.form)
    print('上传数据', request.form)
    if form.validate():
        status = form.status.data
        suggestion = form.suggestion.data
        id = form.id.data
        event = Event_Search_Engine.objects(_id=id).first()
        if event:
            event.status = status
            event.suggestion = suggestion
            event.save()
            return restful.success()
        else:
            return restful.params_error(message='未找到对应的ID')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/review_event/')
@login_required
def review_event():
    return render_template('eog/review_event.html')


@bp.route('/danger_event/')
@login_required
def danger_event():
    return render_template('eog/danger_event.html')


@bp.route('/rules/')
@login_required
def rules():
    if request.method == 'GET':
        rules_count = Rule.objects().count()
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page - 1) * Config.RULE_PER_PAGE
        end = start + Config.RULE_PER_PAGE
        pagination = Pagination(bs_version=3, page=page, total=rules_count, per_page=Config.RULE_PER_PAGE)
        rules = (Rule.objects.order_by('-create_time'))[start:end]
        if rules:
            flash("规则库中共有{}条规则".format(rules_count))
        else:
            flash("查询错误，请检查后再次查询")
        context = {
            "rules": rules,
            "pagination": pagination,
            "rules_count": rules_count
        }
        return render_template('eog/rules.html', **context)


@bp.route('/log/')
@login_required
def log():
    '''
#TODO(李然):添加查询时间段的功能，在 #190`Operate_Log`分页的对象换成查询时间段后的对象
    :return:
    '''
    log_count =Operate_Log.objects().count()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * Config.LOG_PER_PAGE
    end = start + Config.LOG_PER_PAGE
    pagination = Pagination(bs_version=3, page=page, total=log_count, per_page=Config.LOG_PER_PAGE)
    logs = (Operate_Log.objects.order_by('-operate_time'))[start:end]
    context={
        "logs":logs,
        "pagination": pagination,
        "log_count": log_count
    }
    return render_template('eog/operate_log.html',**context)


@bp.route('/source/')
@login_required
def source():
    return render_template('eog/source.html')


@bp.route('/my_review/')
@login_required
def my_review():
    return render_template('eog/my_review.html')


@bp.route('/my_score/')
@login_required
def my_score():
    return render_template('eog/my_score.html')


@bp.route('/user/')
@login_required
def user():
    return render_template('eog/user.html')


@bp.route('/logout/')
@login_required
def logout():
    del session[DevelopmentConfig.CMS_USER_ID]
    NowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logout_signal.send(logout_time=NowTime)
    return redirect(url_for('front.login'))


class LogView(views.MethodView):
    decorators = [login_required]

    def get(self):

        return render_template('eog/my_log.html')

    def post(self):
        date = request.form.get('date')
        print(date)
        if date == None:
            return render_template('eog/my_log.html', date=date)
        else:
            today = date + ' ' + '0:00:00'
            log = Log.objects(today=today, handler=g.eog_user.email).all()
            print(log)
            for i in log:
                print(i.login_time)
            if not log:
                return restful.params_error(message='没有找到当天的登录信息！')
            else:
                return restful.success(data=log)


class ResetPWView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('eog/my_setting.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.eog_user
            if user.password == oldpwd:
                user.password = newpwd
                user.save()
                NowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                change_password_signal.send(operate_time=NowTime, ip=request.remote_addr)
                return restful.success()
            else:
                return restful.params_error('旧密码错误！')
        else:
            message = form.get_error()
            return restful.unauth_error(message=message)


class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('eog/my_setting.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            if User.objects(email=email).first():
                return restful.params_error('该邮箱已经被注册，请选择未被使用的邮箱注册！')
            g.eog_user.email = email
            g.eog_user.save()
            NowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            change_email_signal.send(operate_time=NowTime, ip=request.remote_addr,
                                     operate_detail='修改邮箱为:{}'.format(email))
            return restful.success()
        else:
            return restful.params_error(form.get_error())


class ResetUsernameView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('eog/profile.html')

    def post(self):
        form = ResetUsernameForm(request.form)
        if form.validate():
            username = form.username.data
            g.eog_user.username = username
            g.eog_user.save()
            NowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            change_username_signal.send(operate_time=NowTime, ip=request.remote_addr,
                                        operate_detail='修改用户名为:{}'.format(username))
            return restful.success('用户名修改成功！')
        else:
            return restful.params_error(form.get_error())


def allowd_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class UploadavatarView(views.MethodView):
    decorators = [login_required]

    def get(self):
        ip = request.remote_addr
        return render_template('eog/my_profile.html', user_ip=ip)

    def post(self):
        # file = request.files['avatar_upload']
        file = request.files['avatar_upload']
        base_path = './static/eog/img/user/'
        filename = str(g.eog_user.email) + '.' + file.filename.rsplit('.', 1)[1]
        print(filename)
        if not allowd_file(file.filename):
            return restful.params_error('上传的文件格式不合法，请选择图片格式文件上传！')
        file_path = os.path.join(base_path, filename)
        file.save(file_path)
        g.eog_user.avatar_path = '/static/eog/img/user/' + filename
        g.eog_user.save()
        NowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        change_lcon_signal.send(operate_time=NowTime, ip=request.remote_addr)
        return restful.success('修改头像成功！')


def dateTOtimestamp(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))


class AccountView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('eog/my_log.html')

    def post(self):
        date1 = request.form.get('date1')
        date2 = request.form.get('date2')
        print(date1, date2)
        if date1 == '' and date2 == '':
            return restful.params_error(message='请选择时间范围或者某一天！')
        if date1 == '' and date2 != '':
            return restful.params_error(message='请在第一个时间框内输入，查询当天的信息！')
        if date1:
            if date2:
                if dateTOtimestamp(date1) > dateTOtimestamp(date2):
                    return restful.params_error(message='查询的时间不合法！')
                else:
                    account = Account.objects(operator=g.eog_user.email, today__gte=date1,
                                              today__lte=date2).order_by('-operate_time').all()
                    print(account)
                    if not account:
                        return restful.params_error(message='没有找到这一时间段的账号信息')
                    else:
                        return restful.success(data=account)
            else:
                account = Account.objects(operator=g.eog_user.email,today=date1).order_by('-operate_time').all()
                print(account)
                if not account:
                    return restful.params_error(message='没有找到{}的账号信息'.format(date1))
                else:
                    return restful.success(data=account)


@bp.route('/remove/')
@login_required
def remove():
    tag = request.args.get('tag')
    if tag == '1':
        User.objects(email=g.eog_user.email).delete()
        del session[DevelopmentConfig.CMS_USER_ID]
        flash('账号删除成功！')
        return restful.success()
    else:
        return restful.params_error('传参错误！')


bp.add_url_rule('/account/', view_func=AccountView.as_view('account'))
bp.add_url_rule('/resetpwd/', view_func=ResetPWView.as_view('resetpwd'))
bp.add_url_rule('/resetmail/', view_func=ResetEmailView.as_view('resetmail'))
bp.add_url_rule('/profile/', view_func=UploadavatarView.as_view('profile'))
bp.add_url_rule('/resetusername/', view_func=ResetUsernameView.as_view('resetusername'))
bp.add_url_rule('/my_log/', view_func=LogView.as_view('my_log'))
