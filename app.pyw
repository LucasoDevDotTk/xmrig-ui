import os

# Install requirements.txt
# os.system("pip install -r requirements.txt")

from flask import Flask, render_template, request, redirect
from flaskwebgui import FlaskUI
from flask_socketio import SocketIO, emit
import psutil
from flask_session import Session

# import pyuac

import json
import subprocess
from datetime import datetime
from threading import Lock

from modules import install
from modules import socket
from modules import config
from modules import live_data

# Check if xmrig is installed
if os.path.isdir("xmrig/xmrig-6.19.3") == False:
    install.install_xmrig()

__version__ = "0.1.6"
xmrig_version = "6.19.3"

running = "False"

configured = "False"

start_time = datetime.now()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
Session(app)

# Thread for updating the live data
thread = None
thread_lock = Lock()

# Thread for updating the xmrig output
thread1 = None
thread_lock1 = Lock()

def update_xmrig_output():
    while True:
        try:
            xmrig_output = str(xmrig_prc.stdout.readline().decode("utf-8"))

            socketio.emit('xmrig_output', {'xmrig_output': xmrig_output}, namespace='/')
            print(xmrig_output)

        except Exception as e:
            pass


def update_live_data():
    while True:
        socketio.sleep(1)
        print("Updating live data")
        uptime = int(live_data.calculate_uptime(start_time=start_time))
        cpu_usage = psutil.cpu_percent(percpu=False)
        cpu_freq = psutil.cpu_freq(percpu=False).max
        total_mem = round(psutil.virtual_memory().total/1000000000)
        mem_usage = psutil.virtual_memory().percent

        socketio.emit('live_data', {'uptime': uptime, 'cpu_usage': cpu_usage, 'cpu_freq': cpu_freq, 'total_mem':total_mem, 'mem_usage': mem_usage}, namespace='/')

@app.route('/')
def index():
    if config.check_config() == True:
        configured = "True"
    else:
        configured = "False"
    
    if running == "False":
        try:
            xmrig_prc.kill()
        except:
            pass

    return render_template('index.html', running=running, configured=configured, xmrig_version=xmrig_version, version=__version__)

@app.route('/configuration')
def serve_configuration():
    return render_template('configuration.html', xmrig_version=xmrig_version, version=__version__)

@app.route('/reinstall_xmrig', methods=['POST'])
def reinstall_xmrig():
    install.install_xmrig()
    return redirect('/')

@app.route('/settings')
def configuration():
    return render_template('under_development.html')

@app.route('/documentation')
def documentation():
    return redirect("https://github.com/lucasodevdottk/xmrig-ui/", code=302)

@app.route('/start', methods=['POST'])
def start():
    print("Starting miner")
    global running
    running = "True"

    global xmrig_prc
    xmrig_prc = subprocess.Popen(["./xmrig/xmrig-6.19.3/xmrig"], stdout=subprocess.PIPE)

    return redirect('/')


@app.route('/stop', methods=['POST'])
def stop():
    print("Stopping miner")
    global running
    running = "False"

    global xmrig_prc
    # Stop miner
    xmrig_prc.kill()
    xmrig_prc = None

    return redirect('/')

@app.route('/get_json_config')
def get_json_config():
    return json.dumps(config.get_config(), indent=4)

# Post to /configuration and print content posted
@app.route('/configuration', methods=['POST'])
def configuration_post():
    print(request.form)

    # Get values from form
    donation = request.form['donation']
    if donation == "":
        donation = 0

    donation = int(donation)

    if donation <= 0:
        donation = 1
    elif donation > 100:
        donation = 100

    cpu = False
    opencl = False
    cuda = False

    tls = True
    keepalive = True
    nicehash = False

    coin = request.form['coin']
    if coin == "":
        coin = None

    algo = request.form['algorithm']
    if algo == "":
        algo = None

    pool_domain = request.form['pool']
    pool_port = request.form['pool_port']
    pool = pool_domain + ":" + pool_port

    address = request.form['address']
    password = request.form['password']
    if password == "":
        password = None

    if pool_domain == "" or pool_port == "" or address == "":
        return render_template('configuration.html', error="Please fill in all required fields")

    else:
        try:
            if request.form['cpu'] == "on":
                cpu = True
        except:
            pass

        try:
            if request.form['open_cl'] == "on":
                opencl = True
        except:
            pass

        try:
            if request.form['cuda'] == "on":
                cuda = True
        except:
            pass

        json_config = {"autosave": True, "donate-level": donation, "cpu": cpu, "opencl": opencl, "cuda": cuda, "pools": [
            {
                "coin": coin,
                "algo": algo,
                "url": pool,
                "user": address,
                "pass": password,
                "tls": tls,
                "keepalive": keepalive,
                "nicehash": nicehash
            }
        ]}

        # Write to file
        with open('config.json', 'w') as outfile:
            json.dump(json_config, outfile, indent=4)
            outfile.write("\n")
        
        with open('./xmrig/xmrig-6.19.3/config.json', 'w') as outfile:
            json.dump(json_config, outfile, indent=4)
            outfile.write("\n")

        
        global configured
        configured = "True"

        return redirect('/')

@socketio.on('connect')
def handle_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(update_live_data)
    
    global thread1
    with thread_lock1:
        if thread1 is None:
            thread1 = socketio.start_background_task(update_xmrig_output)


if __name__ == "__main__":

    # if not pyuac.isUserAdmin():
    #     print("Re-launching as admin!")
    #     pyuac.runAsAdmin()
    # else:        

    app.run(debug=True)
    # FlaskUI(app=app, server="flask").run()
