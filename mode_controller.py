import tcp_connection
import principal_thread
import jinglebell
import TEMT6000_sensor
from threading import Thread

# Les print en commentaire c'était pour les test si vous souhaitez voir dans le terminal qu'est-ce que le script envoie

def mode1():
    tcp_connection.send_tcp_message("mode1")
    print("main def mode1 stop")


def mode2():
    tcp_connection.send_tcp_message("mode2")
    print("main def mode2 stop")
