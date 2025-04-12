from threading import Thread
import socket


SERVER_HOST = '10.10.23.212' 
SERVER_PORT = 12347         
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