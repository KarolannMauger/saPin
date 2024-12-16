from rpi_ws281x import PixelStrip, Color
import time

LENLED = 50

strip = PixelStrip(LENLED, 12)
strip.begin()
strip.setBrightness(0)

def fadeinfadeout():
    for b in range(0,51,1):
        strip.setBrightness(b)
        strip.show()
        time.sleep(0.03)
    for b in range(50,-1,-1):
        strip.setBrightness(b)
        strip.show()
        time.sleep(0.03)
        
def start():
    try:
        while True:
            for i in range(LENLED):
                strip.setPixelColor(i, Color(255,0,0))
                strip.show()
            fadeinfadeout()
            for i in range(LENLED):
                strip.setPixelColor(i, Color(0,0,255))
                strip.show()
            fadeinfadeout()
            for i in range(LENLED):
                strip.setPixelColor(i, Color(0,255,0))
                strip.show()
            fadeinfadeout()
    except KeyboardInterrupt:
        for i in range(LENLED):
            strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        print("programme interrompu")