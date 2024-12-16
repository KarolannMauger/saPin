from rpi_ws281x import PixelStrip, Color
import time

LENLED = 50
Y1 = (100,255,0)
R1 = (0,200,0)
B1 = (100,100,255)
B2 = (0,0,255)
C1 = B1
C2 = B2

strip = PixelStrip(LENLED, 18)
strip.begin()
strip.setBrightness(50)

try:
    while True:
        for i in range(LENLED):
            if i%2 == 0:
                strip.setPixelColor(i, Color(C1[0],C1[1],C1[2])) #255,100,0 yellow
            elif i%2 == 1:
                strip.setPixelColor(i, Color(C2[0],C2[1],C2[2])) #200,0,0
        strip.show()
        time.sleep(0.3)
        for j in range(LENLED):
            if j%2 == 0:
                strip.setPixelColor(j, Color(C2[0],C2[1],C2[2]))
            elif j%2 == 1:
                strip.setPixelColor(j, Color(C1[0],C1[1],C1[2]))
        strip.show()
        time.sleep(0.3)
except KeyboardInterrupt:
    for i in range(LENLED):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    print("programme interrompu")


