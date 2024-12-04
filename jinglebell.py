import pigpio
import time
 
# Initialisation de la connexion pigpio
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
   ('E4', 0.5), ('E4', 0.5), ('E4', 1),                  ('E4', 0.5), ('E4', 0.5), ('E4', 1), 
   ('E4', 0.5), ('G4', 0.5), ('C4', 0.5), ('D4', 0.5),   ('E4', 1.5), ('Silence', 0.5),
   ('F4', 0.5), ('F4', 0.5), ('F4', 1),                  ('E4', 0.5), ('E4', 0.5), ('E4', 1),
   ('D4', 0.5), ('D4', 0.5), ('D4', 0.5), ('E4', 0.5),   ('D4', 1), ('G4', 1),
   
   ('E4', 0.5), ('E4', 0.5), ('E4', 1),                  ('E4', 0.5), ('E4', 0.5), ('E4', 1), 
   ('E4', 0.5), ('G4', 0.5), ('C4', 0.5), ('D4', 0.5),   ('E4', 1.5), ('Silence', 0.5),
   ('F4', 0.5), ('F4', 0.5), ('F4', 0.5), ('F4', 0.5),   ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), ('E4', 0.5),
   ('G4', 0.5), ('G4', 0.5), ('F4', 0.5), ('D4', 0.5),   ('C4', 2),
]
 
def play_tone(pin, frequency, duration):
    if frequency == 0:
        time.sleep(duration)
        return
   
    pi.hardware_PWM(pin, frequency, 500000)
    time.sleep(duration)
    pi.hardware_PWM(pin, 0, 0)
 

try:
    print("Playing 'We Wish You a Merry Christmas'...")
    for note, duration in melody:
        frequency = notes.get(note, 0)
        play_tone(BUZZER_PIN, frequency, duration)
        time.sleep(1.0 / 15)
    print("Done!")
except KeyboardInterrupt:
    print("Interrupted!")
    pi.write(BUZZER_PIN, 0)
finally:
    pi.stop()