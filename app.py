from flask import Flask, render_template, request, redirect
from flaskwebgui import FlaskUI

import json
import os
import subprocess

__version__ = "0.1.0"

running = "False"

configured = "False"

app = Flask(__name__)

def get_config():
    with open('config.json') as json_file:
        data = json.load(json_file)
    return data

def check_config():
    try:
        with open('config.json') as json_file:
            data = json.load(json_file)
        return True
    except:
        return False

@app.route('/')
def index():
    if check_config() == True:
        configured = "True"
    else:
        configured = "False"

    return render_template('index.html', running=running, configured=configured)

@app.route('/configuration')
def serve_configuration():
    return render_template('configuration.html')

@app.route('/settings')
def configuration():
    return render_template('under_development.html')

@app.route('/documentation')
def documentation():
    return render_template('under_development.html')

@app.route('/start', methods=['POST'])
def start():
    print("Starting miner")
    global running
    running = "True"

    global xmrig_prc
    xmrig_prc = subprocess.Popen(["./xmrig/xmrig"], cwd="./xmrig")

    return redirect('/')


@app.route('/stop', methods=['POST'])
def stop():
    print("Stopping miner")
    global running
    running = "False"

    # Stop miner
    xmrig_prc.kill()

    return redirect('/')
    

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
        
        with open('./xmrig/config.json', 'w') as outfile:
            json.dump(json_config, outfile, indent=4)
            outfile.write("\n")

        
        global configured
        configured = "True"

        return render_template('configuration.html')

if __name__ == "__main__":
    app.run(debug=True)
    #FlaskUI(app=app, server="flask").run()
