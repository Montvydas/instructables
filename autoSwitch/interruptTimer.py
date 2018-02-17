from machine import Pin
import machine
from time import sleep

# Global value to communicate with the IRQ routine
isAwake = 1

# GPIO16 (D0) is the internal LED for NodeMCU
led = Pin(16, Pin.OUT)

# Callback should be as short as possible
def timer_callback(timer):
    # Require to specify that isPirActive and led are global for this function
    global isAwake, led
    isAwake = True
    # Invert LED value
    led.value(not led.value())

# Using Timer object specify timer type, period in ms and ISR function
timer = machine.Timer(0)
timer.init(period=10000, mode=machine.Timer.PERIODIC, callback=timer_callback)

while True:
    # we want to disable interrupts before using/changing its shared global value
    if isAwake:
        state = machine.disable_irq()
        isAwake = False
        machine.enable_irq(state)

        print("Just Woke Up!")