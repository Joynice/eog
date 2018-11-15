from flask import Flask
from front import bp as front_bp
from common import bp as common_bp
from eog import bp as eog_bp
from config import config, Config
from exts import db, mail
from flask_wtf.csrf import CSRFProtect
import datetime


def create_app(config_env):
    app = Flask(__name__)
    app.config.from_object(config[config_env])
    config[config_env].__init__(app)
    app.register_blueprint(eog_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)
    app.permanent_session_lifetime = datetime.timedelta(seconds=60*60*3)
    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)
    return app


app = create_app('default')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)