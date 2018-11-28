# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, EqualTo, Email, ValidationError, Regexp, InputRequired
from utils import zlcache
from flask import g


class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message

    def validate(self):
        return super(BaseForm, self).validate()


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='密码长度要求大于6位,小于20位'), InputRequired(message='请输入旧密码')])
    newpwd = StringField(validators=[Length(6, 20, message='密码长度要求大于6位,小于20位'), InputRequired(message='请输入新密码')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='确认密码必须和新密码保持一致'), InputRequired(message='请再次输入新密码')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='请输入邮箱')])
    captcha = StringField(validators=[Length(min=6, max=6, message='请输入正确格式的验证码'), InputRequired(message='请输入邮箱验证码')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_cache = zlcache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误')

    def validate_email(self, field):
        email = field.data
        user = g.eog_user
        if user.email == email:
            raise ValidationError('不能使用相同的邮箱进行修改')


class ResetUsernameForm(BaseForm):
    username = StringField(validators=[Length(2, 20, message='请输入正确格式的用户名'), InputRequired(message='请输入用户名')])


class AddSuggesionEvent(BaseForm):
    id = IntegerField(validators=[InputRequired(message='请输入事件id')])
    status = StringField(validators=[InputRequired(message='请选择审核结果')])
    suggestion = StringField()
