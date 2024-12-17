import time
import pigpio
import tcp_connection
import principal_thread
import mode_controller
from threading import Thread



pi = pigpio.pi()
BTN = 27  
pi.set_mode(BTN, pigpio.INPUT)
pi.set_pull_up_down(BTN, pigpio.PUD_UP)

BUZZER_PIN = 18
pi.set_mode(BUZZER_PIN, pigpio.OUTPUT)


cur = pi.read(BTN)
last = cur
count = 0
compteur = 0
isPressed = False

if __name__ == '__main__':
    try:
        tcp_connection.establish_tcp_connection()
        time.sleep(0.5)
        mode_controller.mode2() 
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
                        principal_thread.stop_sensor()  
                        mode_controller.mode2()  
                    else:  
                        principal_thread.stop_sensor()  
                        mode_controller.mode1()  
                    compteur += 1 
                    isPressed = True  

            if cur == 0:  
                isPressed = False

            last = cur  

    except KeyboardInterrupt:
        tcp_connection.send_tcp_message("stop")
        print("\nJoyeux NAEL!!!")
    finally:
        if tcp_connection.client_socket is not None:
            tcp_connection.client_socket.close()
            print("Connexion TCP fermée.")
