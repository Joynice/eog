# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from wtforms import StringField, IntegerField
from wtforms import Form
from wtforms.validators import Regexp, Email, InputRequired, ValidationError, Length, EqualTo
from utils import zlcache


class BaseForm(Form):
    def get_error(self):
        print(self.errors)
        message = self.errors.popitem()[1][0]
        return message

    def validate(self):
        return super(BaseForm, self).validate()


class SignupForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱地址！'),InputRequired(message='请输入邮箱地址')])
    email_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确格式的邮箱验证码！'), InputRequired(message='请输入邮箱验证码')])
    username = StringField(validators=[Length(2, 20, message='请输入正确格式的用户名'), InputRequired(message='请输入用户名')])
    password1 = StringField(validators=[Regexp(r'[0-9a-zA-Z_\./]{6,20}', message='请输入正确格式的密码'), InputRequired(message='请输入密码')])
    password2 = StringField(validators=[EqualTo("password1", message='两次密码输入不同！'), InputRequired(message='请再次输入密码')])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确格式的图形验证码！'), InputRequired(message='请输入图形验证码')])
    realname = StringField(validators=[InputRequired(message='请输入真实姓名'), InputRequired(message='请输入真实姓名')])

    def validate_email_captcha(self, field):
        captcha = field.data
        email = self.email.data
        try:
            captcha_cache = zlcache.get(email)
        except:
            raise ValidationError(message='邮箱验证码不存在！')
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError(message='邮箱验证码错误！')

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        try:
            graph_captcha_mem = zlcache.get(graph_captcha.lower())
        except:
            raise ValidationError(message='图形验证码不存在！')
        print(graph_captcha_mem, graph_captcha)
        if not graph_captcha_mem:
            raise ValidationError(message='图形验证码错误！')


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    remember = IntegerField()


class ForgetpwdForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='请输入邮箱')])
    email_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确格式的邮箱验证码！')])
    password1 = StringField(validators=[Regexp(r'[0-9a-zA-Z_\./]{6,20}', message='请输入正确格式的密码')])
    password2 = StringField(validators=[Regexp(r'[0-9a-zA-Z_\./]{6,20}', message='请输入确认密码')])

    def validate_email_captcha(self, field):
        captcha = field.data
        email = self.email.data
        try:
            captcha_cache = zlcache.get(email)
        except:
            raise ValidationError(message='邮箱验证码不存在！')
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError(message='邮箱验证码错误！')
