import client.tcp_connection as tcp_connection
from threading import Thread

principal_thread = None 
stop_principal_thread = False  

def stop_principal_thread():
    global stop_principal_thread
    stop_principal_thread = True
    if principal_thread is not None and principal_thread.is_alive():
        stop_principal_thread = True
        principal_thread.join()  


def restart_principal_thread(target_name):
    global principal_thread, stop_principal_thread
    stop_principal_thread = False 
    if principal_thread is not None and principal_thread.is_alive():
        stop_principal_thread()  
    principal_thread = Thread(target=target_name, args=(lambda: stop_principal_thread, tcp_connection.client_socket))
    principal_thread.start()