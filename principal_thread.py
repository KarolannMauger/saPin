import tcp_connection
from threading import Thread
import time
import tcp_connection
import queue
import jinglebell
import TEMT6000_sensor
principal_thread = None 
stop_principal_thread = False  

def stop_principal_thread1():
    global stop_principal_thread
    stop_principal_thread = True
    if principal_thread is not None and principal_thread.is_alive():
        stop_principal_thread = True
        principal_thread.join()


def start_principal_thread(data_queue, stop_queue, servo_queue):
    global principal_thread, stop_principal_thread
    stop_principal_thread = False 
    if principal_thread is not None and principal_thread.is_alive():
        stop_principal_thread1()
    principal_thread = Thread(target=principal_thread_fct, args=(lambda: stop_principal_thread, tcp_connection.client_socket, data_queue, stop_queue, servo_queue))
    principal_thread.start()

def principal_thread_fct(arg1,arg2, data_queue, stop_queue, servo_queue):
    
    
    while True:
        try:
            state = data_queue.get_nowait()
            if(state == "mode1"):
                
                jinglebell.start(stop_queue)
            if(state == "mode2"):
                
                TEMT6000_sensor.start(stop_queue, servo_queue)
            # tcp_connection.send_tcp_message("toto")
            time.sleep(0.1)
        except queue.Empty:
            pass