import tcp_connection
import principal_thread
import jinglebell
import TEMT6000_sensor_NeedTCPCall
from threading import Thread


def mode1():
    tcp_connection.send_tcp_message("stop") 
    print("main def mode1 stop")
    principal_thread.stop_sensor()
    principal_thread.restart_principal_thread(jinglebell.start)  
    tcp_connection.send_tcp_message("mode1")
    print("main def mode1 mode1")


def mode2():
    tcp_connection.send_tcp_message("stop")
    print("main def mode2 stop")
    principal_thread.stop_sensor() 
    principal_thread.restart_principal_thread(TEMT6000_sensor_NeedTCPCall.TEMT6000_sensor)