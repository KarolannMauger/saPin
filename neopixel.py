import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D18, 50, brightness=0.5)
pixels.fill((0,255,255))
time.sleep(2)
pixels = neopixel.NeoPixel(board.D18, 50, brightness=0.1)
pixels.fill((0,255,255))
time.sleep(1)
pixels.fill((0,0,0))
pixels.show()
