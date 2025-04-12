import board
import busio
from time import sleep
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_ht16k33 import matrix
from threading import Thread, Event

i2c = busio.I2C(board.SCL, board.SDA)
module = i2c_device.I2CDevice(i2c, 0x70)
mat = matrix.Matrix8x8(i2c)


n0 = 0    
n1 = 24   
n2 = 36   
n3 = 60   
n4 = 90  
n5 = 102  
n6 = 153  
n7 = 231  


p1 = [n0, n0, n0, n1]
p2 = [n0, n0, n3, n2]
p3 = [n0, n4, n3, n5]
p4 = [n6, n4, n3, n7]
p5 = [n1, n4, n3, n7]
p6 = [n1, n1, n3, n7]

pattern_order = [p1, p2, p3, p4, p5, p6, p5, p4, p5, p6, p5, p4,
                 p5, p6, p5, p4, p5, p6, p5, p4, p5, p6, p5, p4,
                 p5, p6, p5, p4, p5, p6, p5, p4, p3, p2, p1]


stop_event = Event()

def light_up_pattern(pattern):
    j = 0
    for i in range(0, 7, 2):
        module.write(bytes([i]))
        module.write(bytes([i, pattern[j]]))
        mir = 14 - i
        module.write(bytes([mir]))
        module.write(bytes([mir, pattern[j]]))
        j += 1
    sleep(0.2)

def start_animation():
    global stop_event
    stop_event.clear()  
    while not stop_event.is_set():  
        for pat in pattern_order:
            if stop_event.is_set():  
                break
            light_up_pattern(pat)
        sleep(0.2)

def stop_animation():
    global stop_event
    stop_event.set()  
    mat.fill(0)  

def start(stop_thread):
    global stop_event
    anim_thread = Thread(target=start_animation)
    anim_thread.start()

    while True:
        if stop_thread():  
            stop_animation() 
            anim_thread.join() 
            break

        
        sleep(0.05) 
