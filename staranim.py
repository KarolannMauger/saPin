import board
import busio
from time import sleep
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_ht16k33 import matrix

i2c = busio.I2C(board.SCL, board.SDA)
module = i2c_device.I2CDevice(i2c, 0x70)
mat = matrix.Matrix8x8(i2c)

# Light what
n0 = 0 #00000000
n1 = 24 #00011000
n2 = 36 #00100100
n3 = 60 #00111100
n4 = 90 #01011010
n5 = 102 #01100110
n6 = 153 #10011001
n7 = 231 #11100111

# Patterns
p1 = [n0, n0, n0, n1]
p2 = [n0, n0, n3, n2]
p3 = [n0, n4, n3, n5]
p4 = [n6, n4, n3, n7]
p5 = [n1, n4, n3, n7]
p6 = [n1, n1, n3, n7]

pattern_order = [p1, p2, p3, p4, 
                 p5, p6, p5, p4, p5, p6, p5, p4,
                 p5, p6, p5, p4, p5, p6, p5, p4,
                 p5, p6, p5, p4, p5, p6, p5, p4,
                 p5, p6, p5, p4, p5, p6, p5, p4,
                 p3, p2, p1]

def light_up_pattern(pattern):
    j = 0
    for i in range(0,7,2):
        module.write(bytes([i]))
        module.write(bytes([i,pattern[j]]))
        #print(str(i)+", "+str(pattern[j]))
        mir = 14 - i
        #print(str(mir)+", "+str(pattern[j]))
        module.write(bytes([mir]))
        module.write(bytes([mir,pattern[j]]))
        j+=1
    print("pattern: "+str(pattern))
    sleep(0.2)

try:
    while True:
        for pat in pattern_order:
            light_up_pattern(pat)
   # mat.fill(0)
except KeyboardInterrupt:
    mat.fill(0)