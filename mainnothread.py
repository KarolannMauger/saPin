import time
import pigpio
import staranim
import jinglebell
import snot2
from threading import Thread
import socket


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


principal_thread = None 
stop_principal_thread = False  

# Connexion TCP
SERVER_HOST = '10.10.21.148' 
SERVER_PORT = 12349         
client_socket = None        


def establish_tcp_connection():
    global client_socket
    try:
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connexion TCP établie.")
    except Exception as e:
        print(f"Erreur lors de l'établissement de la connexion TCP: {e}")


def send_tcp_message(message):
    try:
        if client_socket is not None:
            client_socket.sendall(message.encode())  
            print(f"Message envoyé au serveur: {message}")
        else:
            print("Erreur: Pas de connexion TCP établie.")
    except Exception as e:
        print(f"Erreur lors de l'envoi du message TCP: {e}")


def stop_sensor():
    global stop_principal_thread
    stop_principal_thread = True
    if principal_thread is not None and principal_thread.is_alive():
        stop_principal_thread = True
        principal_thread.join()  


def restart_toto(target_name):
    global principal_thread, stop_principal_thread
    stop_principal_thread = False 
    if principal_thread is not None and principal_thread.is_alive():
        stop_sensor()  
    principal_thread = Thread(target=target_name, args=(lambda: stop_principal_thread,))
    principal_thread.start()


def mode1():
    print('mode1')
    send_tcp_message("stop")  
    stop_sensor() 
    restart_toto(jinglebell.start)  
    send_tcp_message("mode1") 


def mode2():
    print('mode2')
    send_tcp_message("stop") 
    stop_sensor() 
    restart_toto(snot2.toto) 
    send_tcp_message("mode2") 


if __name__ == '__main__':
    try:
        establish_tcp_connection()
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

            
            if cur == 0:  
                isPressed = False

            last = cur  

    except KeyboardInterrupt:
        send_tcp_message("stop")
        print("\nJoyeux NAEL!!!")
    finally:
        if client_socket is not None:
            client_socket.close()
            print("Connexion TCP fermée.")
