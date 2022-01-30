# app.py

# also importing the request module
from flask import Flask, render_template, request
import sys,os
import configparser
import dbus
from sense_hat import SenseHat

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../../config/rgb_options.ini')

# Configuration for the matrix
config = configparser.ConfigParser()
config.read(filename)

sysbus = dbus.SystemBus()
systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
sense = SenseHat()

# home route
@app.route("/")
def saved_config():
    power = config['DEFAULT']['power']
    lowlight = config['DEFAULT']['lowlight']
    return render_template('index.html', power = power, lowlight = lowlight)

# handling power status
@app.route("/power", methods=["GET", "POST"])
def handle_power():
    power = request.form['power']
    lowlight = config['DEFAULT']['lowlight']    
    config.set('DEFAULT', 'power', request.form['power'])
    if power == 'on':
      job = manager.StartUnit('spotipi.service', 'replace')
    else:
      job = manager.StopUnit('spotipi.service', 'replace')
      sense.clear()
    return render_template('index.html', power = power, lowlight = lowlight)

# handling light status
@app.route("/lowlight", methods=["GET", "POST"])
def handle_lowlight():
    power = config['DEFAULT']['power']
    lowlight = request.form['lowlight']
    config.set('DEFAULT', 'lowlight', request.form['lowlight'])
    if lowlight == 'on':
      sense.low_light = True
    else:
      sense.low_light = False
    return render_template('index.html', power = power, lowlight = lowlight)


app.run(host='0.0.0.0', port=80) 

