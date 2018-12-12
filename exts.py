from flask_mongoengine import MongoEngine
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_principal import Principal

principal = Principal()
socketio = SocketIO()
db = MongoEngine()
mail = Mail()