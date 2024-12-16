import socket
import threading
import queue
from rpi_ws281x import PixelStrip, Color
import time

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)

# Queue to store data received by threads
data_queue = queue.Queue()

# Function to handle receiving data for each client in a separate thread
def handle_client(connection, client_address):
    print(f"Connection from {client_address} established.")
    try:
        while True:
            data = connection.recv(1024)  # Try to read up to 1024 bytes
            if not data:
                print(f"Client {client_address} has closed the connection.")
                break
            print(f"Received data: {data.decode()} from {client_address}")
            
            # Put the received data into the queue to be used by the main thread
            data_queue.put((client_address, data.decode()))

    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        connection.close()
        print(f"Connection with {client_address} closed.")

LENLED = 50

strip = PixelStrip(LENLED, 12)
strip.begin()
strip.setBrightness(0)

def fadeinfadeout():
    for b in range(0,51,1):
        strip.setBrightness(b)
        strip.show()
        if shouldStop():
            ledClose()
            return True
        time.sleep(0.03)
    for b in range(50,-1,-1):
        strip.setBrightness(b)
        strip.show()
        if shouldStop():
            ledClose()
            return True
        time.sleep(0.03)
    return False
def ledClose():
    for i in range(LENLED):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show() 
def shouldStop():
    try:
        # Try to get data from the queue without blocking
        client_address, data = data_queue.get_nowait()
        # Process the data here
        print(f"Main thread processing data from {client_address}: {data}")
        
        # Simulate some processing
        time.sleep(0.1)  # Simulate time spent processing data
        data_queue.task_done()
        if data == "stop":
            return True
        return False
    except queue.Empty:
        # If the queue is empty, we don't block and just continue processing other things
        pass

def start():
    try:
        while True:
            print("Start")
            for i in range(LENLED):
                strip.setPixelColor(i, Color(255,0,0))
                strip.show()
            if fadeinfadeout():
                break
           
    except KeyboardInterrupt:
        ledClose()
        print("programme interrompu")



connection, client_address = server_socket.accept()
# Start a new thread for each client to handle communication
client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
client_thread.daemon = True  # This allows the thread to exit when the main program exits
client_thread.start()

# Main server loop to accept client connections
while True:

    try:
        # Try to get data from the queue without blocking
        client_address, data = data_queue.get_nowait()
        # Process the data here
        print(f"Main thread processing data from {client_address}: {data}")
        
        # Simulate some processing
        time.sleep(0.1)  # Simulate time spent processing data
        data_queue.task_done()
        if data == "mod1":
            start()
    except queue.Empty:
        # If the queue is empty, we don't block and just continue processing other things
        pass
    except KeyboardInterrupt:
        print("Closing serveur")
        # client_thread.stop()
        connection.close()
        server_socket.close()
        break
    # Sleep for a short time to allow other tasks to run and prevent 100% CPU usage
    # time.sleep(0.1)

