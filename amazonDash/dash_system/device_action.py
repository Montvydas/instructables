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
