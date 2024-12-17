import pigpio
import time
import staranim
from threading import Thread


pi = pigpio.pi()
BUZZER_PIN = 18
pi.set_mode(BUZZER_PIN, pigpio.OUTPUT)

##https://www.seventhstring.com/resources/notefrequencies.html
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


def start(stop_thread, client_socket):
    anim_thread = None
    stop_anim_thread = False
    
    
    def start_animation():
        staranim.start(lambda: stop_anim_thread)
    
    while True:
        if stop_thread(): 
            if anim_thread is not None and anim_thread.is_alive():
                stop_anim_thread = True
                anim_thread.join()  
            break

        
        if anim_thread is None or not anim_thread.is_alive():
            stop_anim_thread = False
            anim_thread = Thread(target=start_animation)
            anim_thread.start()

        
        for note, duration in melody:
            frequency = notes.get(note, 0)
            play_tone(BUZZER_PIN, frequency, duration)
            time.sleep(1.0 / 15)  
            if stop_thread(): 
                break
        
        time.sleep(1)
