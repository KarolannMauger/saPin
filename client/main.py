import time
import pigpio
import client.tcp_connection as tcp_connection
import client.principal_thread as principal_thread
import client.mode_controller as mode_controller
from threading import Thread
import queue
import client.servo_motor as servo_motor

data_queue = queue.Queue()
stop_queue = queue.Queue()
servo_queue = queue.Queue()

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
is_pressed = False

if __name__ == '__main__':
    try:
        tcp_connection.establish_tcp_connection()
        time.sleep(0.5)
        principal_thread.start_principal_thread(data_queue, stop_queue, servo_queue)  
        servo_thread = Thread(target=servo_motor.rotate_servo, args=(servo_queue,))
        servo_thread.start()
        time.sleep(0.5)
        mode_controller.mode2()
        data_queue.put("mode2")

        while True:
            cur = pi.read(BTN)

            if cur == 0:
                if not is_pressed: 
                    if count < 4: 
                        count += 1
                    elif count == 4:  
                        count = 0 
                        if compteur % 2 != 0:  
                            stop_queue.put("stop")
                            servo_queue.put("stop") 

                            time.sleep(1)
                            mode_controller.mode2()  
                            data_queue.put("mode2")

                        else:  
                            stop_queue.put("stop")
                            servo_queue.put("stop") 

                            time.sleep(1)
                            mode_controller.mode1()
                            data_queue.put("mode1")

                        compteur += 1 
                        is_pressed = True  

            if cur == 1:  
                is_pressed = False
                count = 0
            last = cur  

    except KeyboardInterrupt:
        tcp_connection.send_tcp_message("stop")
        principal_thread.stop_principal_thread1() 
        servo_queue.put("stop")
        servo_thread.join() 
        print("\nJoyeux NAEL!!!")
    finally:
        principal_thread.stop_principal_thread1() 
        servo_queue.put("stop") 
        servo_thread.join() 

        if tcp_connection.client_socket is not None:
            tcp_connection.client_socket.close()

            print("Connexion TCP fermée.")
