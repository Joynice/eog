from flask_mongoengine import MongoEngine
from flask_mail import Mail
from flask_socketio import SocketIO
socketio = SocketIO()
db = MongoEngine()
mail = Mail()