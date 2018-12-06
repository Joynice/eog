# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from flask import Blueprint, views, render_template, request, url_for, redirect, session
from .forms import SignupForm, LoginForm, ForgetpwdForm
from .models import User
from signals import login_signal, forget_password_signal
from utils import restful, safeutils
import config
from datetime import datetime

bp = Blueprint("front", __name__, url_prefix='/front')


@bp.route('/')
def index():
    return 'front html'


class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/signup.html', return_to=return_to)
        else:
            return render_template('front/signup.html')

    def post(self):
        form = SignupForm(request.form)
        print(form)
        print(form.email.data)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password1.data
            realname = form.realname.data
            print(email)
            user = User(email=email, username=username, realname=realname)
            user.password = password
            user.save()
            return restful.success()
        else:
            # print(form.get_error())

            return restful.server_error(message=form.get_error())


class LoginView(views.MethodView):
    def get(self, message=None):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for('front.signup') and \
                safeutils.is_safe_url(return_to):
            return render_template('front/login.html', return_to=return_to, message=message)
        else:
            return render_template('front/login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = User.objects(email=email).first()
            if user and user.check_password(password):
                session[config.DevelopmentConfig.CMS_USER_ID] = user._id  # 保存用户登录信息
                ip = request.remote_addr
                NowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                login_signal.send(ip=ip, handler=email, login_time=NowTime)
                if remember:
                    # 如果设置session.permanent = True，那么过期时间为31天
                    session.permanent = True
                return redirect(url_for('eog.index'))
            else:
                return self.get(message='邮箱或者密码错误')

        else:
            # print(form.errors)
            message = form.get_error()
            return self.get(message=message)


# @bp.route('/email_captcha/')
# def email_captcha():
#     email = request.args.get('email')
#     params = request.referrer.split('/')[-2]
#     print(email)
#     print(params)
#     regex = '^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$'
#     if not re.match(regex, email):
#         return restful.params_error('请输入正确格式的邮箱！')
#     if not email:
#         return restful.params_error('请传递邮箱参数！')
#     elif params == 'signup' and User.objects(email=email).first():
#         return restful.params_error('邮箱已经被注册，请更换邮箱!')
#     elif User.objects(email=email).first() and (params == 'resetpwd' or params == 'resetmail'):
#         return restful.params_error('该邮箱已经被注册，请更换邮箱！')
#     elif not User.objects(email=email).first() and params == 'forgetpwd':
#         return restful.params_error('该邮箱没有被注册过，请先注册！')
#     else:
#         source = list(string.ascii_letters)
#         source.extend(map(lambda x: str(x), range(0, 10)))
#         captcha = "".join(random.sample(source, 6))
#         print(captcha)
#         message = Message('专家值守平台邮箱验证码', recipients=[email], body='您的验证码是：{}'.format(captcha))
#         print(message)
#     try:
#         mail.send(message)
#     except Exception as e:
#         return restful.server_error(message='可能邮箱不存在！请检查后再试')
#     zlcache.set(email, captcha)
#     return restful.success()


class Forgetpwd(views.MethodView):

    def get(self):
        return render_template('front/forgetpwd.html')

    def post(self):
        form = ForgetpwdForm(request.form)
        if form.validate():
            email = form.email.data
            if form.password1.data != form.password2.data:
                return restful.params_error('两次密码输入不同，请重新确认！')
            password = form.password1.data
            user = User.objects(email=email).first()
            user.password = password
            user.save()
            NowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            forget_password_signal.send(operate_time=NowTime, ip=request.remote_addr, operator=email, operate_detail='重置密码')
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/forgetpwd/', view_func=Forgetpwd.as_view('forgetpwd'))