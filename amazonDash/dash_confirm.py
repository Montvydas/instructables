from scapy.all import *
import requests
from datetime import datetime

# a single press will be 10 minutes
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from datetime import timedelta
import time


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


class TimedDevice:
    def __init__(self, device, job_id, trigger_on="turn_on", trigger_off="turn_off", hours=0, minutes=0, seconds=0):
        self.device = device
        # how long should a single click run for
        self.trigger_on = trigger_on
        self.trigger_off = trigger_off
        self.timeout = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        self.scheduler = scheduler
        self.job_id = job_id

    def set_timeout(self, hours=0, minutes=0, seconds=0):
        self.timeout = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def stop_timer(self):
        # get the job by the id
        job = self.get_job()
        # if job exists, remove it and trigger the set off action
        if job:
            getattr(self.device, self.trigger_off)()
            job.remove()

    def start_timer(self):
        # get the job by the id
        job = self.get_job()
        # if we don't have a job, make one
        if job is None:
            now = datetime.now()
            # Set the trigger OFF function
            self.scheduler.add_job(getattr(self.device, self.trigger_off),
                                   trigger='date', run_date=now + self.timeout, id=self.job_id)
            # now trigger the ON action
            getattr(self.device, self.trigger_on)()
        else:
            print "Job is already started!"

    def add_extra(self):
        # get the job by the id
        job = self.get_job()
        # if job exists, add extra
        if job:
            self.scheduler.reschedule_job(self.job_id, trigger='date', run_date=job.next_run_time + self.timeout)
            print "Added EXTRA"

    def get_job(self):
        return self.scheduler.get_job(self.job_id)

    def start_or_add_timer(self):
        if self.get_job() is None:
            self.start_timer()
        else:
            self.add_extra()


class DeviceAction:
    def __init__(self, device, mac, action):
        self.device = device
        self.mac = mac
        self.action = action

    def get_device(self):
        return self.device

    def get_mac(self):
        return self.mac

    def get_action(self):
        return self.action


class DevicesWithActions:
    def __init__(self):
        self.devices_with_actions = []

    def add_device_with_action(self, device_with_action):
        self.devices_with_actions.append(device_with_action)

    def get_from_mac(self, mac):
        """
        Gets all of the devices with their action function names
        matching the given MAC. This allows one device to perform multiple actions.

        @param mac  the mac address of the dash button

        return list of devices with actions
        """
        devices = []
        for dev in self.devices_with_actions:
            if dev.get_mac() == mac:
                devices.append(dev)
        return devices

# create parent function with passed in arguments
def control_devices(devices_with_actions, scheduler):
    # arp_detect has access to the passed devices and their actions

    def arp_detect(packet):
        # upload packet, using passed arguments
        if packet[ARP].op == 1:  # network request
            # get both the device corresponding to the received MAC and the delay_job
            devices = devices_with_actions.get_from_mac(packet[ARP].hwsrc)
            job = scheduler.get_job("delay_job")

            # if any device was found and delay_job finished running, then do:
            if devices and not job:
                # Add a delay job of several seconds to make sure that if we receive
                # multiples of the same signals, they would be discarded
                # When that job finishes it calls lambda: None, which basically does nothing
                timeout = datetime.now() + timedelta(seconds=2)
                scheduler.add_job(lambda: None, trigger='date', run_date=timeout, id="delay_job")

                for dev in devices:
                    print 'Received', dev.get_action(), 'request from', dev.get_device().get_name()

                    # Finally call by name. This requires a device e.g. TimedDevice, IftttDevice and
                    # the functions name to be called e.g. start_timer, turn_on, toggle.
                    getattr(dev.get_device(), dev.get_action())()

    return arp_detect


if __name__ == "__main__":
    key = "YOUR IFTTT KEY GOES HERE"
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Crete an object to store all of our devices
    devices_with_actions = DevicesWithActions()

    # Create Heater: requires name, ifttt key, event name for turning it on & off.
    # Also make the heater timed. Use default function names for trigger_on and off
    # and set the timeout to be several minutes.
    # Finally we specify the functions to be launched when the button is pressed to be
    # start_or_add_timer. This will add another several minutes to the already running timer
    # ff the button was pressed and timer already running or start the timer if it wasn't running.
    heater = IftttDevice('Heater', key, 'heater_on', 'heater_off')
    timedHeater = TimedDevice(heater, scheduler, "heater_job", seconds=5)
    heater_action = DeviceAction(timedHeater, 'fc:a6:67:4c:ad:d9', 'start_or_add_timer')
    devices_with_actions.add_device_with_action(heater_action)

    # Create Desk Lamp: same as heater however only device_toggle event name is specified.
    # It is not timed thus don't create TimerDevice. Enter action name to be toggle.
    desk_lamp = IftttDevice('Desk Lamp', key, device_toggle='toggle_desk_lamp')
    desk_lamp_action = DeviceAction(desk_lamp, 'fc:a6:67:27:83:2e', 'toggle')
    devices_with_actions.add_device_with_action(desk_lamp_action)

    print "Started Listening..."
    print sniff(prn=control_devices(devices_with_actions, scheduler), filter="arp", store=0)
