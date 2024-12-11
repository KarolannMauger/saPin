import time
import pigpio
import snot2
import jinglebell
from threading import Thread
 
BTN = 27

 
pi = pigpio.pi()
cur = pi.read(BTN)
 
last = cur
compteur = 0
count = 0
isPressed = False
isAllume = True
 
 
principal_thread = None
stop_principal_thread = False
 
 
def stop_sensor():
    global stop_principal_thread
    stop_principal_thread = True  
 
 
def restart_toto(target_name):
    global principal_thread, stop_principal_thread
    stop_principal_thread = False  
    if principal_thread is not None and principal_thread.is_alive():
        print("Arrêt du thread principal précédent.")
        stop_sensor()
        principal_thread.join()  
    principal_thread = Thread(target=target_name, args=(lambda: stop_principal_thread,))
    principal_thread.start()


def mode1():
    print('mode1')
    stop_sensor()  
    global principal_thread
    if principal_thread is not None and principal_thread.is_alive():
        principal_thread.join()
        restart_toto(jinglebell.start)  
    if stop_principal_thread:
        stop_sensor()
        return  

def mode2():
    global principal_thread
    print('mode2')
    if principal_thread is None or not principal_thread.is_alive():
        restart_toto(snot2.toto)  
    if stop_principal_thread:
        stop_sensor()
        return  
 
 
if __name__ == '__main__':
    try:
        mode2()
        while True:
            cur = pi.read(BTN)
 
            if not isPressed:
                if cur == 1:
                    count = 0
                elif count < 4:
                    count += 1
                elif count == 4:
                    count = 0
                    if compteur % 2 != 0:  
                        print("Changement vers mode2")
                        stop_sensor()  
                        mode2()
                    else:  
                        print("Changement vers mode1")
                        stop_sensor()  
                        mode1()
                    compteur += 1
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