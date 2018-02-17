from machine import Pin
from time import sleep

# GPIO4 (D2) is our PIR pin
pir = Pin(4, Pin.IN, Pin.PULL_UP)
# GPIO16 (D0) is the internal LED for NodeMCU
led = Pin(16, Pin.OUT)
# Wait for the PIR sensor to calibrate for 20s
# sleep(20)

# Loop just as in Arduino
while True:
    # set the LED value to be identical to what we read from PIR
    led.value(pir.value())
    # sleep for 0.1 of a second
    sleep(0.1)