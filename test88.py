import board
import busio
from time import sleep
import adafruit_bus_device.i2c_device as i2c_device

i2cBus = busio.I2C(board.SCL, board.SDA)
module = i2c_device.I2CDevice(i2cBus, 0x70)

octetAffiche = 165 #10100101
for i in range(0,16,2):
    module.write(bytes([i])) # Spécifier l'adresse qui sera utilisée
    module.write(bytes([i,octetAffiche])) # Écrire les données à l'adresse
    sleep(1)
    module.write(bytes([i,0])) # Écrire les données (vides) à l'adresse