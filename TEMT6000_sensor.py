import busio
import board
import time
import pigpio
import time



from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.ads1115 import P0
from adafruit_ads1x15.analog_in import AnalogIn

## We have to set the GPIO of the led
LED=1
pi = pigpio.pi()
pi.set_mode(LED,pigpio.OUTPUT)

## The voltage is 5v
TENSION = 5

'''
We need to find a better variable name. 
This variable is used to set the minimum voltage to turn on or off the led. 
It can't be 0, since there is already ambient light in the room.
'''
LOW = 1


i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS1115(i2c, 2/3)

data = AnalogIn(ads, P0)


pi.write(LED, 0)


while True:
    try:

        if (data.voltage > LOW):
            pi.write(LED, 1)
        else:
            pi.write(LED, 0)
        ## Not necessary
        print(data.value, data.voltage)
        time.sleep(0.5)
    except KeyboardInterrupt:
        pi.write(LED, 0)
        break