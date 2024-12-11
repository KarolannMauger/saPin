import pigpio
from time import sleep

servo = 17 # Le numéro GPIO de la broche ou est connecté le servomoteur
FREQ = 50 # Fréquence en Hz de la période

pi = pigpio.pi()
pi.set_mode(servo,pigpio.OUTPUT)
pi.set_PWM_frequency(servo,FREQ)
pi.set_PWM_range(servo,100) # Valeurs possibles dutycycle de 0-100

plus90 = 12.5
moins90 = 2.5

def rotate_servo(stop_servo_thread):
    while True:
        if stop_servo_thread():
            print("LIGHT ON")
            break

        print("servo")
        pi.set_PWM_dutycycle(servo,plus90)
        sleep(1)
        pi.set_PWM_dutycycle(servo,moins90)
        sleep(1)
