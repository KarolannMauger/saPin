from rpi_ws281x import PixelStrip, Color
import pigpio
import time

LENLED = 50

strip = PixelStrip(LENLED, 12)
strip.begin()
strip.setBrightness(50)

pi = pigpio.pi()
BUZZER_PIN = 18
pi.set_mode(BUZZER_PIN, pigpio.OUTPUT)

pi = pigpio.pi()
pi.set_mode(18,pigpio.OUTPUT)

i = int(input('entrer nombre: '))

while i > 0:
    
    pi.write(18,1)
    time.sleep(1)
    pi.write(18,0)
    time.sleep(1)
    i -= 1