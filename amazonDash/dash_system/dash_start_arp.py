from scapy.all import *
from datetime import datetime
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from ifttt_device import IftttDevice
from dash_action import DashActions, DashAction
from timed_device import TimedDevice

# create parent function with passed in arguments
def control_devices(dash_actions, scheduler):
    # arp_detect has access to the passed devices and their actions

    def arp_detect(packet):
        # upload packet, using passed arguments
        if packet[ARP].op == 1:  # network request
            # get both the device corresponding to the received MAC and the delay_job
            actions = dash_actions.get_from_mac(packet[ARP].hwsrc)
            job = scheduler.get_job("delay_job")

            # if any actions were found and delay_job finished running, then do:
            if actions and not job:
                # Add a delay job of several seconds to make sure that if we receive
                # multiples of the same signals, they would be discarded
                # When that job finishes it calls lambda: None, which basically does nothing
                timeout = datetime.now() + timedelta(seconds=2)
                scheduler.add_job(lambda: None, trigger='date', run_date=timeout, id="delay_job")

                for action in actions:
                    # print some data about what action was received
                    action.print_info()
                    # Finally call the registered action
                    action.press()

    return arp_detect


if __name__ == "__main__":
    key = "YOUR IFTTT KEY GOES HERE"
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Crete an object to store all of our actions
    dash_actions = DashActions()

    # Create Heater: requires name, ifttt key, event name for turning it on & off.
    # Also make the heater timed. Use default function names for trigger_on and off
    # and set the timeout to be several minutes.
    # Finally we specify the functions to be launched when the button is pressed to be
    # start_or_add_timer. This will add another several minutes to the already running timer
    # of the button was pressed and timer already running or start the timer if it wasn't running.
    heater = IftttDevice('Heater', key, 'heater_on', 'heater_off')
    timed_heater = TimedDevice(heater, scheduler, "heater_job", seconds=5)
    heater_action = DashAction(timed_heater, 'fc:a6:67:4c:ad:d9', 'start_or_add_timer')
    dash_actions.register(heater_action)

    # Create Desk Lamp: same as heater however only device_toggle event name is specified.
    # It is not timed thus don't create TimerDevice. Enter action name to be toggle.
    desk_lamp = IftttDevice('Desk Lamp', key, device_toggle='toggle_desk_lamp')
    desk_lamp_action = DashAction(desk_lamp, 'fc:a6:67:27:83:2e', 'toggle')
    dash_actions.register(desk_lamp_action)

    print "Started Listening..."
    print sniff(prn=control_devices(dash_actions, scheduler), filter="arp", store=0)
