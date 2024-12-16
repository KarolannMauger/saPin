import busio
import board
import time
import pigpio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.ads1115 import P0
from adafruit_ads1x15.analog_in import AnalogIn
from threading import Thread
import servo_motor
 
#LED = 12
pi = pigpio.pi()
#pi.set_mode(LED, pigpio.OUTPUT)
 
TENSION = 5
LOW = 1
 
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c, 2/3)
data = AnalogIn(ads, P0)
 
#pi.write(LED, 0)

 
 
def toto(stop_toto):
    servo_thread = None
    stop_servo_thread = False
    while True:
        if stop_toto():
            if servo_thread is not None and servo_thread.is_alive():
                stop_servo_thread = True
                servo_thread.join()
            break  
 
       
        if data.voltage < LOW:
            print("low")
            ##Call TCP LED yes
            if servo_thread is None or not servo_thread.is_alive():
                stop_servo_thread = False
                servo_thread = Thread(target=servo_motor.rotate_servo, args=(lambda: stop_servo_thread,))
                servo_thread.start()
        else:
            print("hight")
            ##Call TCP LED no
            if servo_thread is not None and servo_thread.is_alive():
                stop_servo_thread = True
                servo_thread.join()
        print(data.value, data.voltage)
        time.sleep(0.5)