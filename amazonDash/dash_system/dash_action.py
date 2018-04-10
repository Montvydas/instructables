class DashAction:
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
    
    def press(self):
        getattr(self.device, self.action)()

    def print_info(self):
        print 'Received', self.action, 'request on', self.device.get_name()


class DashActions:
    def __init__(self):
        self.dash_actions = []

    def register(self, dash_action):
        self.dash_actions.append(dash_action)

    def get_from_mac(self, mac):
        """
        Gets all of the actions with their action function names
        matching the given MAC. This allows one device to perform multiple actions.

        @param mac  the mac address of the dash button

        return list of dash actions
        """
        actions = []
        for act in self.dash_actions:
            if act.get_mac() == mac:
                actions.append(act)
        return actions
