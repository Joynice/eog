# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from flask import Blueprint, request, make_response
from utils import restful
from utils.captcha import Captcha
from io import BytesIO
import string
import random
from utils import zlcache
import re
from front.models import User
from tasks import send_mail
bp = Blueprint("common", __name__, url_prefix='/c')


@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    print(text.lower())
    zlcache.set(text.lower(), text.lower())
    print(zlcache.get(text.lower()))
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    params = request.referrer.split('/')[-2]
    print(email)
    print(params)
    regex = '^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$'
    if not re.match(regex, email):
        return restful.params_error('请输入正确格式的邮箱！')
    if not email:
        return restful.params_error('请传递邮箱参数！')
    elif params == 'signup' and User.objects(email=email).first():
        return restful.params_error('邮箱已经被注册，请更换邮箱!')
    elif User.objects(email=email).first() and (params == 'resetpwd' or params == 'resetmail'):
        return restful.params_error('该邮箱已经被注册，请更换邮箱！')
    elif not User.objects(email=email).first() and params == 'forgetpwd':
        return restful.params_error('该邮箱没有被注册过，请先注册！')
    else:
        source = list(string.ascii_letters)
        source.extend(map(lambda x: str(x), range(0, 10)))
        captcha = "".join(random.sample(source, 6))
        print(captcha)
    try:
        send_mail.delay('专家值守平台邮箱验证码', recipients=[email], body='您的验证码是：{}'.format(captcha))
    except Exception as e:
        return restful.server_error(message='邮箱不存在！请检查后再试')
    zlcache.set(email, captcha)
    return restful.success()
