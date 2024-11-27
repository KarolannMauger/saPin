from rpi_ws281x import PixelStrip, Color
import time

LENLED = 50

strip = PixelStrip(LENLED, 18)
strip.begin()

try:
    for i in range(LENLED):
        strip.setPixelColor(i, Color(255,255,255))
    strip.show
    while True:
        for i in range(LENLED):
            for j in range(LENLED):
                if i == j:
                    strip.setPixelColor(j, Color(0,255,0))
                    #strip.show(0
                else:
                    strip.setPixelColor(j, Color(255,255,255))
                    #strip.show()
                strip.show()
            time.sleep(0.2)
        for i in range(LENLED):
            strip.setPixelColor(i, Color(255,255,255))
        strip.show
except KeyboardInterrupt:
    for i in range(LENLED):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    print("programme interrompu")

