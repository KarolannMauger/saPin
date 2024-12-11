import time
import pigpio
from threading import Thread
import led_music
##import matrix_display
##import lcd_message
import TEMT6000_sensor

BTN = 27
pi = pigpio.pi()
cur = pi.read(BTN)

last = cur
compteur = 0
count = 0
isPressed = False

principal_thread = None
stop_principal_thread = False

def stop_sensor():
    global stop_principal_thread
    stop_principal_thread = True  

def restart_principal_thread():
    global principal_thread, stop_principal_thread
    stop_principal_thread = False  
    if principal_thread is not None and principal_thread.is_alive():
        stop_sensor()
        principal_thread.join()  
    principal_thread = Thread(target=TEMT6000_sensor.start, args=(lambda: stop_principal_thread,))
    principal_thread.start()

def mode1():
    led_music_thread = Thread(target=led_music.start)
    ##matrix_thread = Thread(target=matrix_display.start)
    ##lcd_thread = Thread(target=lcd_message.start)

    led_music_thread.start()
    ##matrix_thread.start()
    ##lcd_thread.start()

    led_music_thread.join()
    ##matrix_thread.join()
    ##lcd_thread.join()

def mode2():
    global principal_thread

    if principal_thread is None or not principal_thread.is_alive():
        restart_principal_thread()  

    if stop_principal_thread:
        stop_sensor()
        return

if __name__ == '__main__':
    try:
        while True:
            cur = pi.read(BTN)

            if not isPressed:
                if cur == 1:
                    count = 0
                elif count < 4:
                    count += 1
                elif count == 4:
                    compteur += 1
                    count = 0
                    if compteur % 2 != 0:
                        stop_sensor()  
                        mode2()
                    else:
                        stop_sensor()  
                        mode1()
                    isPressed = True
            else:
                if cur == 0:  
                    count = 0
                elif count < 4:
                    count += 1
                elif count == 4:
                    count += 1
                    isPressed = False

            last = cur
    except KeyboardInterrupt:
        print("\nJoyeux NAEL!!!")
