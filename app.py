from flask import Flask, render_template
from front import bp as front_bp
from common import bp as common_bp
from eog import bp as eog_bp
from config import config
from exts import db, mail
from flask_wtf.csrf import CSRFProtect
import datetime
from flask_socketio import SocketIO
from utils import zlcache
from threading import Lock
thread = None
async_mode = None
thread_lock = Lock()


def create_app(config_env):
    app = Flask(__name__)
    app.config.from_object(config[config_env])
    config[config_env].__init__(app)
    app.register_blueprint(eog_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)
    app.permanent_session_lifetime = datetime.timedelta(seconds=60 * 60 * 3)
    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)
    return app


app = create_app('default')
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/<id>/')
def index(id):
    zlcache.socket_set(key='key', value=id)
    return render_template('eog/chart.html', async_mode=socketio.async_mode)


def get_date():
    count = 0
    while True:
        socketio.sleep(5)
        id = int(zlcache.socket_get(key='key'))
        date = zlcache.socket_get(id)
        date_list = eval(date)
        count += 1
        socketio.emit('server_response', {'data': date_list}, namespace='/test')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=get_date)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)
