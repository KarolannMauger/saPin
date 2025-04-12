import busio
import board
import time
import pigpio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.ads1115 import P0
from adafruit_ads1x15.analog_in import AnalogIn
from threading import Thread
import client.servo_motor as servo_motor
 

pi = pigpio.pi()
LOW = 1
 
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c, 2/3)
data = AnalogIn(ads, P0)

# Les print en commentaire c'était pour les test si vous souhaitez voir dans le terminal qu'est-ce que le script envoie

 
def start(stop_TEMT6000_sensor, client_socket):
    servo_thread = None
    stop_servo_thread = False
    while True:

        if stop_TEMT6000_sensor():
            if servo_thread is not None and servo_thread.is_alive():
                stop_servo_thread = True
                servo_thread.join()
            break  
 
       
        if data.voltage < LOW:
            if servo_thread is None or not servo_thread.is_alive():
                stop_servo_thread = False
                client_socket.sendall("mode2".encode())
                #print("sensor mode2")
                servo_thread = Thread(target=servo_motor.rotate_servo, args=(lambda: stop_servo_thread,))
                servo_thread.start()

        else:
            if servo_thread is not None and servo_thread.is_alive():
                stop_servo_thread = True
                servo_thread.join()
                client_socket.sendall("stop".encode())
                #print("sensor stop")
        print(data.value, data.voltage)
        time.sleep(0.5)