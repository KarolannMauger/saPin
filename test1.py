from rpi_ws281x import PixelStrip, Color
import pigpio
import time



 
# Initialisation de la connexion pigpio
pi = pigpio.pi()
BUZZER_PIN = 18
pi.set_mode(BUZZER_PIN, pigpio.OUTPUT)


LENLED = 50

strip = PixelStrip(LENLED, 12)
strip.setBrightness(50)
strip.begin()

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


color_table = {
    'E4': (255, 255, 255),  
    'G4': (255, 0, 0),     
    'C4': (0, 255, 0),      
    'D4': (255, 255, 0),    
    'F4': (0, 0, 255),    
    'Silence': (0, 0, 0),   
}
 
def play_tone(pin, frequency, duration):
    if frequency == 0:
        time.sleep(duration)
        return
   
    pi.hardware_PWM(pin, frequency, 500000)
    time.sleep(duration)
    pi.hardware_PWM(pin, 0, 0)
 

def change_color(strip, LENLED, r, g, b):
    for i in range(LENLED):
        strip.setPixelColor(i, Color(r, g, b))
    strip.show()




try:
    print("Playing 'Jingle Bell'...")
    for note, duration in melody:
        frequency = notes.get(note, 0)

        if note in color_table:
            r, g, b = color_table[note]
            change_color(strip, LENLED, r, g, b)

        play_tone(BUZZER_PIN, frequency, duration)
        time.sleep(1.0 / 15)
    print("Done!")
except KeyboardInterrupt:
    print("Interrupted!")
    pi.write(BUZZER_PIN, 0)
    for i in range(LENLED):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()