# -*- coding: UTF-8 -*-
__author__ = 'Joynice'

from celery import Celery
from flask_mail import Message
from exts import mail
from flask import Flask
import config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
mail.init_app(app)


"""
celery 启动命令:celery -A tasks.celery worker --pool=solo --loglevel=info， 启动时保证与tasks.py同级
若出现 'AttributeError: 'float' object has no attribute 'items'错误，这是redis包版本不兼容，退回2.10.6版本即可。
pip install redis==2.10.6
"""


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task
def send_mail(subject, recipients, body):
    message = Message(subject=subject, recipients=recipients, body=body)
    mail.send(message)
