from pydhcplib.dhcp_network import *
from apscheduler.schedulers.background import BackgroundScheduler

from ifttt_device import IftttDevice
from dash_action import DashActions, DashAction
from timed_device import TimedDevice


netopt = {'client_listen_port': "68", 'server_listen_port': "67", 'listen_address': "0.0.0.0"}

class Server(DhcpServer):
    def __init__(self, options):
        DhcpServer.__init__(self, options["listen_address"],
                            options["client_listen_port"],
                            options["server_listen_port"])

    def HandleCustomDhcpRequest(self):
        packet = self.GetNextDhcpPacket()
        if packet:
            return self.hwaddr_to_str(packet.GetHardwareAddress())
        return None

    def hwaddr_to_str(self, hwaddr):
        result = []
        hexsym = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
        for iterator in range(6):
            result += [str(hexsym[hwaddr[iterator] / 16] + hexsym[hwaddr[iterator] % 16])]
        return ':'.join(result)


if __name__ == "__main__":
    key = "YOUR IFTTT KEY GOES HERE"

    scheduler = BackgroundScheduler()
    scheduler.start()

    # Crete an object to store all of our dash actions
    dash_actions = DashActions()

    # Create Heater: requires name, ifttt key, event name for turning it on & off.
    # Also make the heater timed. Use default function names for trigger_on and off
    # and set the timeout to be several minutes.
    # Finally we specify the functions to be launched when the button is pressed to be
    # start_or_add_timer. This will add another several minutes to the already running timer
    # of the button was pressed and timer already running or start the timer if it wasn't running.
    heater = IftttDevice('Heater', key, 'heater_on', 'heater_off')
    timedHeater = TimedDevice(heater, scheduler, "heater_job", seconds=5)
    heater_action = DashAction(timedHeater, 'fc:a6:67:4c:ad:d9', 'start_or_add_timer')
    dash_actions.register(heater_action)

    # Create Desk Lamp: same as heater however only device_toggle event name is specified.
    # It is not timed thus don't create TimerDevice. Enter action name to be toggle.
    desk_lamp = IftttDevice('Desk Lamp', key, device_toggle='toggle_desk_lamp')
    desk_lamp_action = DashAction(desk_lamp, 'fc:a6:67:27:83:2e', 'toggle')
    dash_actions.register(desk_lamp_action)

    print "Started Listening..."

    server = Server(netopt)
    while True:
        mac = server.HandleCustomDhcpRequest()
        actions = dash_actions.get_from_mac(mac)

        # if any device was found, then do:
        for action in actions:
            # print some data about what action was received
            action.print_info()
            # Finally call the registered action
            action.press()
