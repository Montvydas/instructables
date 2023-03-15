from machine import Pin
import machine
from time import sleep

# Global value to communicate with the IRQ routine
isPirActive = 1

# GPIO16 (D0) is the internal LED for NodeMCU
led = Pin(16, Pin.OUT)

# Callback should be as short as possible
def pir_callback(pin):
    # Require to specify that isPirActive and led are global for this function
    global isPirActive, led
    isPirActive = True
    # Set LED to the interrupted pin value
    led.value(pin.value())

# GPIO4 (D2) is our PIR INPUT pin
pir = Pin(4, Pin.IN, Pin.PULL_UP)
# Specify our interrupt service routine function
pir.irq(trigger=Pin.IRQ_RISING, handler=pir_callback)

# Wait for the PIR sensor to calibrate for 20s
sleep(20)

# Loop just as in Arduino
while True:
    # we want to disable interrupts before using/changing its shared global value
    if isPirActive:
        state = machine.disable_irq()
        isPirActive = False
        machine.enable_irq(state)

        print('PIR activated!')
    # sleep for 0.1 of a second
    sleep(0.1)
