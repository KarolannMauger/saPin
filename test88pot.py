import board
import busio
import pigpio
from time import sleep
from adafruit_ads1x15.ads1115 import P0
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_bus_device.i2c_device as i2c_device


def allumeLed88(module,total):
    number = int(total)
    nbRows = (number // 8) + 1

    # Allumer les rangées pleines
    for row in range(0, (nbRows-1)* 2,2):
        module.write(bytes([row,255])) 

    # Allumer la rangée partiellement pleine
    module.write(bytes([(nbRows -1 ) * 2,transform(total)])) 

    # Éteindre les autres
    for row in range((nbRows)* 2, 16 ,2):
        module.write(bytes([row,0])) 
    
def transform(numb):
    nbAllume = int(numb) % 8
    if(numb > 63.5):
        return 0b11111111
    match nbAllume:
        
        case 1:
            return 0b00000001
        case 2:
            return 0b00000011
        case 3:
            return 0b00000111
        case 4:
            return 0b00001111
        case 5:
            return 0b00011111
        case 6:
            return 0b00111111
        case 7:
            return 0b01111111

    return 0b00000000
       

i2cBus = busio.I2C(board.SCL, board.SDA)

led88 = i2c_device.I2CDevice(i2cBus,0x70)

# Init ADS1115
# On utilise le même bus, c'est seulement l'adresse qui change
ads = ADS1115(i2cBus,2/3)
data = AnalogIn(ads, P0)

# Init GPIO
pi = pigpio.pi()

MAX = 4.6
MIN = 0.2
# Test
while True:
    try:
        curVolt = data.voltage
        print(curVolt)
        sleep(0.05)
        allumeLed88(led88,min(max((curVolt-MIN)/MAX * 64,0),63.99))

        

    except KeyboardInterrupt:
        for row in range(0,16,2):
            led88.write(bytes([row,0])) # Écrire les données à l'adresse
        exit()
