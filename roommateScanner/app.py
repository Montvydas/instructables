#!/usr/bin/env python

from flask import Flask
from flask import request
import argparse
from scanhosts import scan
import threading
import requests

app = Flask(__name__)

IFTTT_KEY = 'mma-Sm-C2-5uIh0c3kDBsyvnqk4kRxCwBanNGxDLIpf'
FLATMATES = [
    {'name': 'Justas', 'mac': '64:A2:F9:B8:C9:62'},
    {'name': 'Monty', 'mac': '94:65:2D:26:E1:57'}]
PASSWORD = 'SOME_PASSWORD'
available_flatmates = []

def send_notification(event, iftttkey, flatmates):
    url = 'https://maker.ifttt.com/trigger/{}/with/key/{}'.format(event, iftttkey)
    r = requests.post(url, json={"value1": 'At home: ' + ', '.join(flatmates)})
    # status code for error is 200
    if r.status_code != 200:
        return 'Error, could not send data to IFTTT Webhooks service!'
    print (r.text)
    r.close()

    return 'Successfully sent the request!'

@app.route("/", methods=['GET'])
def load_front_page():
    if request.args.get('password') != PASSWORD:
        return 'Wrong password!'

    print('Loaded front page...')
    # send_notification('rich-notification-event', IFTTT_KEY, available_flatmates) 
    return 'At home: ' + ', '.join(available_flatmates)

@app.route("/api/flatmates", methods=['GET'])
def get_available_flatmates():
    if request.args.get('password') != PASSWORD:
        return 'Wrong password!'
    print('Getting available devices...')
    send_notification('rich-notification-event', IFTTT_KEY, available_flatmates)
    send_notification('request-to-text', IFTTT_KEY, available_flatmates)
    return 'At home: ' + ', '.join(available_flatmates)

def scan_devices(modemip):
    print('Scanning devices...')
    global available_flatmates
    hosts = scan(modemip)
    available_flatmates = [f['name'] for f in FLATMATES for h in hosts if h['mac'] == f['mac']]
    print('Finished scanning, found:')
    print('\n'.join(available_flatmates))
    threading.Timer(60, scan_devices, [modemip]).start()

if __name__ == '__main__':
    print('Starting a server...')
    parser = argparse.ArgumentParser()
    parser.add_argument("modemip", help="Modem IP address including e.g. 192.168.0.1/24")
    args = parser.parse_args()

    scan_devices(args.modemip)
    app.run(host='0.0.0.0', port=80)