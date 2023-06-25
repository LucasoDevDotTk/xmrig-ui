from flask_socketio import SocketIO, emit
from flask_session import Session
import psutil

from threading import Lock

from modules import live_data

def init_socket(app):
    socketio = SocketIO(app, cors_allowed_origins='*')
    # Session(app)

    return socketio


def update_live_data(socketio, start_time):
    while True:
        socketio.sleep(1)
        print("Updating live data")
        uptime = int(live_data.calculate_uptime(start_time=start_time))
        cpu_usage = psutil.cpu_percent(percpu=False)
        print(psutil.cpu_percent())
        socketio.emit('live_data', {'uptime': 100, 'cpu_usage': cpu_usage}, namespace='/')