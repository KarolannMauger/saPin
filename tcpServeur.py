import socket
import threading
import queue
from rpi_ws281x import PixelStrip, Color
import time

LEN_LED = 50
Y1 = (100,255,0)
R1 = (0,200,0)
B1 = (100,100,255)
B2 = (0,0,255)
C1 = Y1
C2 = R1

strip = PixelStrip(LEN_LED, 12)
strip.begin()

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12349))
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


def fade_in_fade_out():
    for b in range(0,51,1):
        strip.setBrightness(b)
        strip.show()
        if should_stop():
            led_close()
            return True
        time.sleep(0.03)
    for b in range(50,-1,-1):
        strip.setBrightness(b)
        strip.show()
        if should_stop():
            led_close()
            return True
        time.sleep(0.03)
    return False

def bi_color():
        for i in range(LEN_LED):
            if i%2 == 0:
                strip.setPixelColor(i, Color(C1[0],C1[1],C1[2])) #255,100,0 yellow
            elif i%2 == 1:
                strip.setPixelColor(i, Color(C2[0],C2[1],C2[2])) #200,0,0
        strip.show()
        time.sleep(0.3)
        for j in range(LEN_LED):
            if j%2 == 0:
                strip.setPixelColor(j, Color(C2[0],C2[1],C2[2]))
            elif j%2 == 1:
                strip.setPixelColor(j, Color(C1[0],C1[1],C1[2]))
        strip.show()
        time.sleep(0.3)
        if should_stop():
            led_close()
            return True
        return False

def led_close():
    for i in range(LEN_LED):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()

def should_stop():
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

def start_mode1():
    try:
        strip.setBrightness(50)
        while True:
            if bi_color():
                break
    except KeyboardInterrupt:
        led_close()
        print("programme interrompu")

def start_mode2():
    try:
        strip.setBrightness(0)
        while True:
            for i in range(LEN_LED):
                strip.setPixelColor(i, Color(255,0,0))
                strip.show()
            if fade_in_fade_out():
                break 
            for i in range(LEN_LED):
                strip.setPixelColor(i, Color(0,255,0))
                strip.show()
            if fade_in_fade_out():
                break 
            for i in range(LEN_LED):
                strip.setPixelColor(i, Color(0,0,255))
                strip.show()
            if fade_in_fade_out():
                break          
    except KeyboardInterrupt:
        led_close()
        print("programme interrompu")



connection, client_address = server_socket.accept()
# start_mode2 a new thread for each client to handle communication
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
        if data == "mode1":
            start_mode1()
        elif data == "mode2":
            start_mode2()
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

