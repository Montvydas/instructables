try:
    import urequests as requests
except ImportError:
    import requests


def turn_lights_on():
    url = 'https://maker.ifttt.com/trigger/motion_detected/with/key/mma-Sm-C2-5uIh0c3kDBsyvnqk4kRxCwBanNGxDLIpf'
    # request type e.g. get, post, put, delete
    r = requests.post(url)
    # status code for error is 200
    if r.status_code != 200:
        return 'Error, could not send data to IFTTT Webhooks service!'
    print (r.text)
    r.close()

    return 'Successfully turned on the lights!'


print (turn_lights_on())
