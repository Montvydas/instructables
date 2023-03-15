#!/usr/bin/env python

import nmap
import argparse

def scan(modemip):
    hosts = []
    nm = nmap.PortScanner()
    nm.scan(hosts=modemip, arguments='-sn -PE')

    for host in nm.all_hosts():
        try:
            name = nm[host]['hostnames'][0]['name']
        except KeyError:
            name = 'unknown'
        try:
            mac = nm[host]['addresses']['mac']
        except KeyError:
            mac = 'unknown'
        try:
            vendor = nm[host]['vendor'][mac]
        except KeyError:
            vendor = 'unknown'

        info = {'mac': mac, 'ip': host, 'vendor': vendor, 'name': name}
        hosts.append(info)

    return hosts


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("modemip", help="Modem IP address including e.g. 192.168.0.1/24")
    args = parser.parse_args()
    
    hosts = scan(args.modemip)

    for host in hosts:
        print (host)

    print('Total Hosts:', len(hosts))
