import pigpio
from time import sleep
import queue
servo = 17
FREQ = 50 

pi = pigpio.pi()
pi.set_mode(servo,pigpio.OUTPUT)
pi.set_PWM_frequency(servo,FREQ)
pi.set_PWM_range(servo,100)

plus90 = 12.5
moins90 = 2.5

def rotate_servo(servo_queue):

    active = False
    while True:
        try:
            data = servo_queue.get_nowait()
            print(data)
            if( data == "stop"):
                active = False
                
            elif (data == "start"):
                active=True
        except queue.Empty:
            pass
        sleep(0.05)
        while active:
            try:
                data = servo_queue.get_nowait()
                print(data)

                if( data == "stop"):
                    active = False

                    break
                elif (data == "start"):
                    pass
            except queue.Empty:
                pass

            
            pi.set_PWM_dutycycle(servo,plus90)
            sleep(1)

            try:
                data = servo_queue.get_nowait()
                print(data)

                if( data == "stop"):
                    active = False
                    break
                elif (data == "start"):
                    pass
            except queue.Empty:
                pass

            pi.set_PWM_dutycycle(servo,moins90)
            sleep(1)

        
