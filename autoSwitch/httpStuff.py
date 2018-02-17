import socket
import time
import machine
from pairwise import Pairwise
import network
import ujson
import urequests


def is_device_home(url, device):
    n = len(device)
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    result = False

    pairwise = Pairwise()

    # return HTTP request to the url text in bytes
    while True:
        data = s.recv(n)

        if not data:
            break

        pairwise.add_next(data)
        if pairwise.contains(device):
            result = True
            break
    s.close()
    return result


def http_post(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('POST /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    # data = s.read()
    # print(str(data, 'utf8'), end='')
    s.close()


with open('data.json', 'r') as openfile:
    json_data = ujson.load(openfile)

ap_url = json_data["ap_url"]
device = json_data["device"]
webhook_url = json_data["webhook_url"]

sta_if = network.WLAN(network.STA_IF)

while True:
    # Make a request to the modem to query all of the connected devices
    if sta_if.isconnected() and is_device_home(ap_url, device):
        print ("Welcome home!")
    else:
        print ("I guess you're not home yet...")
    time.sleep(5)