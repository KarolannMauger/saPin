from rpi_ws281x import PixelStrip, Color
import time

LEN_LED = 50

strip = PixelStrip(LEN_LED, 12)
strip.begin()
strip.setBrightness(0)

def fade_in_fade_out():
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
            for i in range(LEN_LED):
                strip.setPixelColor(i, Color(255,0,0))
                strip.show()
            fade_in_fade_out()
            for i in range(LEN_LED):
                strip.setPixelColor(i, Color(0,0,255))
                strip.show()
            fade_in_fade_out()
            for i in range(LEN_LED):
                strip.setPixelColor(i, Color(0,255,0))
                strip.show()
            fade_in_fade_out()
    except KeyboardInterrupt:
        for i in range(LEN_LED):
            strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        print("programme interrompu")
start()