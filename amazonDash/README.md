# Intro

This project allows to easily use Amazon dash buttons to control your smart home appliances. Control is done through IFTTT service thus you will firstly gonna have to create actions within Webhook service to enable device control using dash buttons. 

# Running The Script

Older dash buttons used ARP packets while the new ones use DHCP, thus two scripts are provided. If you are unsure which button do you own, simply try running both scripts, but I suggest you starting from DHCP one. To start listening for dash buttons simply do:

`sudo python dash_start_dhcp.py`

`sudo python dash_start_arp.py`


# Required Installation

Both scripts will be using APScheduler, thus require to install that:

Mac: `pip install --user apchesduler`
Linux: `sudo pip install apscheduler`

ARP script requires Scapy and tcpdump:

Mac: `pip install --user scapy`
`brew install tcpdump`

Linux: `sudo pip install scapy`
`sudo apt-get install tcpdump`

DHCP script requires pydhcplib:

Mac: `pip install --user pydhcplib`
Linux: `sudo pip install pydhcplib`

# Known Issues

I encountered some issues when running the scripts on Mac and Linux (Raspbian). Firstly, Both scripts were working with the new version of the dash buttons, however only around 50% of the presses were detected, which is quite annoying. Not really sure what the problem is here. On Linux the ARP script didn't catch any packets coming from dash buttons however DHCP packets were caught every single time, thus I would REALLY recommend using Linux in this case with DHCP script.


