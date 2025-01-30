import pigpio
import time
import matrice_animation
from threading import Thread
import queue
import tcp_connection

pi = pigpio.pi()
BUZZER_PIN = 18
pi.set_mode(BUZZER_PIN, pigpio.OUTPUT)

#https://www.seventhstring.com/resources/notefrequencies.html
notes = {
   'E4': 329,
   'G4': 392,
   'C4': 261,
   'D4': 293,
   'F4': 349,
   'Silence': 0
}


melody = [
   ('E4', 0.5), ('E4', 0.5), ('E4', 1), ('E4', 0.5),
   ('E4', 0.5), ('E4', 1), ('E4', 0.5), ('G4', 0.5),
   ('C4', 0.5), ('D4', 0.5), ('E4', 1.5), ('Silence', 0.5),
   ('F4', 0.5), ('F4', 0.5), ('F4', 1), ('E4', 0.5),
   ('E4', 0.5), ('E4', 1), ('D4', 0.5), ('D4', 0.5),
   ('D4', 0.5), ('E4', 0.5), ('D4', 1), ('G4', 1),
  
]


def play_tone(pin, frequency, duration):
    if frequency == 0:
        time.sleep(duration)
        return

    pi.hardware_PWM(pin, frequency, 500000)
    time.sleep(duration)
    pi.hardware_PWM(pin, 0, 0)


def start(stop_queue):
    while not stop_queue.empty():
        stop_queue.get()
    anim_thread = None
    stop_anim_thread = False
    
    
    def start_animation():
        matrice_animation.start(lambda: stop_anim_thread)
    quit = False
    while True:
        # if stop_jinglebell_thread(): 
        #     if anim_thread is not None and anim_thread.is_alive():
        #         stop_anim_thread = True
        #         anim_thread.join()  
        #     break

        
        if anim_thread is None or not anim_thread.is_alive():
            stop_anim_thread = False
            anim_thread = Thread(target=start_animation)
            anim_thread.start()

        i = 0
        for note, duration in melody:
            frequency = notes.get(note, 0)
            tcp_connection.send_tcp_message(str(i))
            i += 1
            play_tone(BUZZER_PIN, frequency, duration)
            time.sleep(1.0 / 15)  
            try:
                if stop_queue.get_nowait() == "stop": 
                    quit = True
                    break
            except queue.Empty:
                pass
        if quit:
            stop_anim_thread = True
            anim_thread.join()
            break
        
        time.sleep(1)
