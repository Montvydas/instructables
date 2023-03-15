import re
import requests
import json


def get_available_devices(url):
    result = []
    # return HTTP request to the url text
    html = requests.get(url).text
    # search for the occurence of a specific text attach_dev = '...ALL_DEVICE_INFO_HERE...';
    m = re.search('attach_dev = \'(.+?)\';', html)
    # if occurence was found, split the device by the delimeter <lf>
    if m:
        result = m.group(1).split("<lf>")
    return result


def get_available_flatmates(flatmates, available_devices):
    available_flatmates = []
    # go through all of flatmates
    for flatmate in flatmates:
        name = flatmate["name"]
        device = flatmate["device"]
        # If the device, belonging to the flatmate is found in available_devices, append list
        if device in available_devices:
            available_flatmates.append(name)
    return available_flatmates

# Firstly read the json file to get flatmate devices
json_data = json.load(open('flatmates.json'))
flatmates = json_data["flatmates"]

# Make a request to the modem to query all of the connected devices
devices = get_available_devices('http://192.168.0.1/')
# Print for debugging
print "Available Devices:"
print devices
print
print "Available Flatmates:"
# Finally get the available flatmates and print the result
available_flatmates = get_available_flatmates(flatmates, devices)

# What happens if there are no flatmates at home?
if not available_flatmates:
    available_flatmates.append("No one is at home - party time!")

# Use join operation to put the flatmate together separated by a comma
print ', '.join(available_flatmates)
