from flask_socketio import SocketIO, emit
from flask_session import Session

def init_socket(app):
    socketio = SocketIO(app, cors_allowed_origins='*')
    Session(app)
