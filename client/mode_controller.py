import client.tcp_connection as tcp_connection
import client.principal_thread as principal_thread
import client.jinglebell as jinglebell
import client.TEMT6000_sensor as TEMT6000_sensor
from threading import Thread

# Les print en commentaire c'était pour les test si vous souhaitez voir dans le terminal qu'est-ce que le script envoie

def mode1():
    tcp_connection.send_tcp_message("stop") 
    #print("main def mode1 stop")
    principal_thread.stop_principal_thread()
    principal_thread.restart_principal_thread(jinglebell.start)  
    tcp_connection.send_tcp_message("mode1")
    #print("main def mode1 mode1")


def mode2():
    tcp_connection.send_tcp_message("stop")
    #print("main def mode2 stop")
    principal_thread.stop_principal_thread() 
    principal_thread.restart_principal_thread(TEMT6000_sensor.start)