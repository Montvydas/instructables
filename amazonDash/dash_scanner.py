# linux: pip install scapy
# mac: pip install --user scapy

from scapy.all import *

def arp_display(packet):
    if packet[ARP].op == 1:
        # It seems that amazon dash wouldn't sent ARP probes 
        # or at least I couldn't pick them up, so this is
        # a workaround - just get all packets and display them
        print "Packet from: " + packet[ARP].hwsrc
        if packet[ARP].psrc == '0.0.0.0': # ARP Probe
            print "ARP Probe from: " + packet[ARP].hwsrc

# Stop this with ctrl + C
print sniff(prn=arp_display, filter="arp", store=0, count=10)