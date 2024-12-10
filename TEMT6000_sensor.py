import busio
import board
import time
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn
from threading import Thread
##Revoir pour le nom
import servo_motor
import led_control

LOW = 1
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c, gain=2/3)
data = AnalogIn(ads, ADS1115.P0)

def start(stop_sensor_thread):
    servo_thread = None
    stop_servo_thread = False

    while True:
        if stop_sensor_thread():
            if servo_thread is not None and servo_thread.is_alive():
                stop_servo_thread = True
                servo_thread.join()
            led_control.turn_off()
            break

        if data.voltage < LOW:
            led_control.turn_on()
            if servo_thread is None or not servo_thread.is_alive():
                stop_servo_thread = False
                servo_thread = Thread(target=servo_motor.rotate_servo, args=(lambda: stop_servo_thread,))
                servo_thread.start()
        else:
            led_control.turn_off()
            if servo_thread is not None and servo_thread.is_alive():
                stop_servo_thread = True
                servo_thread.join()

        print(data.value, data.voltage)
        time.sleep(0.1)
