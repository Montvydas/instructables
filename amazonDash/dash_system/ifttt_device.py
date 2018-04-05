import requests


class IftttDevice:
    def __init__(self, name,  ifttt_key, device_on=None, device_off=None, device_toggle=None):
        self.ifttt_key = ifttt_key
        self.device_on = device_on
        self.device_off = device_off
        self.device_toggle = device_toggle
        self.name = name

    def turn_on(self):
        self.send_event(self.device_on)

    def turn_off(self):
        self.send_event(self.device_off)

    def toggle(self):
        self.send_event(self.device_toggle)

    def get_name(self):
        return self.name

    def send_event(self, event_name):
        url = 'https://maker.ifttt.com/trigger/' + event_name + '/with/key/' + self.ifttt_key
        # request type e.g. get, post, put, delete
        r = requests.post(url)
        # status code for error is 200
        if r.status_code != 200:
            return 'Error, could not reach IFTTT Webhooks to set the', self.name, 'event', event_name
        r.close()
        print 'Sent to', self.name, 'event', event_name
