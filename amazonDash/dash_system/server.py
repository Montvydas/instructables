from pydhcplib.dhcp_network import *


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
