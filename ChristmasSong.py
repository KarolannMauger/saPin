import pigpio
import time
 
# Initialisation de la connexion pigpio
pi = pigpio.pi()
BUZZER_PIN = 18
pi.set_mode(BUZZER_PIN, pigpio.OUTPUT)
 
# Fréquences des notes (en Hz)
notes = {
   'B3': 247,
   'C4': 262,
   'D4': 294,
   'E4': 330,
   'F4': 349,
   'G4': 392,
   'A4': 440,
   'B4': 494,
   'C5': 523
}
 
 
melody = [
   ('B3', 0.4), ('E4', 0.4), ('E4', 0.4), ('F4', 0.4), ('E4', 0.4), ('D4', 0.4), ('C4', 0.4),
   ('C4', 0.4), ('D4', 0.4), ('E4', 0.4), ('A4', 0.4), ('G4', 0.4), ('G4', 0.6),
   ('C4', 0.4), ('E4', 0.4), ('E4', 0.4), ('F4', 0.4), ('E4', 0.4), ('D4', 0.4), ('C4', 0.4),
   ('A4', 0.4), ('C5', 0.4), ('B4', 0.4), ('G4', 0.4), ('A4', 0.8)
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
        time.sleep(0.1)
    print("Done!")
except KeyboardInterrupt:
    print("Interrupted!")
    pi.write(BUZZER_PIN, 0)
finally:
    pi.stop()