import busio
import board
import time
import pigpio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.ads1115 import P0
from adafruit_ads1x15.analog_in import AnalogIn
from threading import Thread
import client.servo_motor as servo_motor
import queue
import client.tcp_connection as tcp_connection

pi = pigpio.pi()
LOW = 1
 
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c, 2/3)
data = AnalogIn(ads, P0)

# Les print en commentaire c'était pour les test si vous souhaitez voir dans le terminal qu'est-ce que le script envoie


def start(stop_queue, servo_queue):
    lastState = "stop"
    while not stop_queue.empty():
        stop_queue.get()

    quit = False

    while True:

       
 
        if data.voltage < LOW:
            if(lastState == 'stop'):
                servo_queue.put("start")
                tcp_connection.send_tcp_message("mode3")
                lastState = 'start'


        else:

            if lastState == 'start':
                tcp_connection.send_tcp_message("mode4")
                servo_queue.put("stop")
                lastState = 'stop'
        print(data.value, data.voltage)
        try:
            if stop_queue.get_nowait() == "stop": 
                servo_queue.put("stop")

                break
        except queue.Empty:
            pass

        time.sleep(0.5)