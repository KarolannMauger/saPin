from rpi_ws281x import PixelStrip, Color
import time

LENLED = 50

strip = PixelStrip(LENLED, 18)
strip.begin()
strip.setBrightness(100)

try:
    while True:
        for i in range(LENLED):
            if i%3 == 0:
                strip.setPixelColor(i, Color(255,0,0))
            elif i%3 == 1:
                strip.setPixelColor(i, Color(0,255,0))
            elif i%3 == 2:
                strip.setPixelColor(i, Color(0,0,255))
        strip.show()
        time.sleep(0.5)
        for j in range(LENLED):
            if j%3 == 0:
                strip.setPixelColor(j, Color(0,255,0))
            elif j%3 == 1:
                strip.setPixelColor(j, Color(0,0,255))
            elif j%3 == 2:
                strip.setPixelColor(j, Color(255,0,0))
        strip.show()
        time.sleep(0.5)
        for k in range(LENLED):
            if k%3 == 0:
                strip.setPixelColor(k, Color(0,0,255))
            elif k%3 == 1:
                strip.setPixelColor(k, Color(255,0,0))
            elif k%3 == 2:
                strip.setPixelColor(k, Color(0,255,0))
        strip.show()
        time.sleep(0.5)
except KeyboardInterrupt:
    for i in range(LENLED):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    print("programme interrompu")

