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
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)

# Queue to store data received by threads
data_queue = queue.Queue()
mode1_queue = queue.Queue()
mode2_queue = queue.Queue()


#https://www.seventhstring.com/resources/notefrequencies.html
note_couleurs = {
   'E4': Color(34, 120, 57),
   'G4': Color(100, 20, 57),
   'C4': Color(40, 0, 200),
   'D4': Color(43, 43, 8),
   'F4': Color(200, 200, 200),
   'Silence': Color(0, 0, 0)
}

melody = [
   ('E4', 0.5), ('G4', 0.5), ('C4', 1), ('D4', 0.5),
   ('E4', 0.5), ('G4', 0.5), ('C4', 1), ('D4', 0.5),
   ('C4', 0.5), ('D4', 0.5), ('E4', 1.5), ('Silence', 0.5),
   ('E4', 0.5), ('G4', 0.5), ('C4', 1), ('D4', 0.5),
   ('E4', 0.5), ('G4', 0.5), ('C4', 1), ('D4', 0.5),
   ('E4', 0.5), ('G4', 0.5), ('C4', 1), ('D4', 0.5),
]

def led_close():
    for i in range(LEN_LED):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    
def play_light(color, duration):
    if color == None:
        led_close()

        time.sleep(duration+0.1)
        return
    time.sleep(duration - 0.1)

def setCouleur(couleur):
    for i in range(LEN_LED):
        strip.setPixelColor(i, couleur)
        strip.show()



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


def fade_in_fade_out(mode2_queue):
    for b in range(0,51,1):
        strip.setBrightness(b)
        strip.show()
        try:
            if mode2_queue.get_nowait() == "stop":
                led_close()
                return True
            time.sleep(0.03)
        except queue.Empty:
            pass
    for b in range(50,-1,-1):
        strip.setBrightness(b)
        strip.show()
        try:
            if mode2_queue.get_nowait() == "stop":
                led_close()
                return True
            time.sleep(0.03)
        except queue.Empty:
            pass
    return False

def start_mode2(mode2_queue):
    try:
        active = False
        while True:
            
            try:
                data = mode2_queue.get_nowait()
                if( data == "stop"):
                    active = False
                    
                elif (data == "start"):
                    active=True
            except queue.Empty:
                pass
            if active:
                active=False
                strip.setBrightness(0)
                while True:
                    for i in range(LEN_LED):
                        strip.setPixelColor(i, Color(255,0,0))
                        strip.show()
                    if fade_in_fade_out(mode2_queue):

                        break 
                    for i in range(LEN_LED):
                        strip.setPixelColor(i, Color(0,255,0))
                        strip.show()
                    if fade_in_fade_out(mode2_queue):
                        break 
                    for i in range(LEN_LED):
                        strip.setPixelColor(i, Color(0,0,255))
                        strip.show()
                    if fade_in_fade_out(mode2_queue):
                        break          
    except KeyboardInterrupt:
        led_close()
        print("programme interrompu")



connection, client_address = server_socket.accept()
# start_mode2 a new thread for each client to handle communication
client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
client_thread.daemon = True  # This allows the thread to exit when the main program exits
client_thread.start()


mode2_thread = threading.Thread(target=start_mode2, args=(mode2_queue,))
mode2_thread.daemon = True  # This allows the thread to exit when the main program exits
mode2_thread.start()

# Main server loop to accept client connections
while True:

    try:
        # Try to get data from the queue without blocking
        client_address, data = data_queue.get_nowait()
        # Process the data here
        print(f"Main thread processing data from {client_address}: {data}")
        
        # Simulate some processing
        time.sleep(0.01)  # Simulate time spent processing data
        if data == "mode1":
            mode2_queue.put("stop")
            # mode1_queue.put("start")
        elif data == "mode2":
            mode1_queue.put("stop")
            led_close()
        elif data == "mode3":
            mode2_queue.put("start")
        elif data == "mode4":
            mode2_queue.put("stop")
            led_close()
            
        elif(int(data) < 100):
            strip.setBrightness(30)
            couleur, duration = melody[int(data)]
           
            for i in range(LEN_LED):
                strip.setPixelColor(i, note_couleurs[couleur])
            strip.show()
            
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

