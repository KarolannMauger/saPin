from rpi_ws281x import PixelStrip, Color

import time
from threading import Thread

LEN_LED = 50

strip = PixelStrip(LEN_LED, 12)
strip.begin()
strip.setBrightness(30)



#https://www.seventhstring.com/resources/notefrequencies.html
note_couleurs = {
   'E4': Color(34, 120, 57),
   'G4': Color(100, 20, 57),
   'C4': Color(40, 0, 200),
   'D4': Color(43, 43, 8),
   'F4': Color(200, 200, 200),
   'Silence': None
}
notes = {
   'E4': 329,
   'G4': 392,
   'C4': 261,
   'D4': 293,
   'F4': 349,
   'Silence': 0
}
def led_close():
    for i in range(LEN_LED):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    
def play_light(color, duration):
    if color == None:
        led_close()

        time.sleep(duration)
        

        return

    
    time.sleep(duration)

    

melody = [
   ('E4', 0.5), ('E4', 0.5), ('E4', 1), ('E4', 0.5),
   ('E4', 0.5), ('E4', 1), ('E4', 0.5), ('G4', 0.5),
   ('C4', 0.5), ('D4', 0.5), ('E4', 1.5), ('Silence', 0.5),
   ('F4', 0.5), ('F4', 0.5), ('F4', 1), ('E4', 0.5),
   ('E4', 0.5), ('E4', 1), ('D4', 0.5), ('D4', 0.5),
   ('D4', 0.5), ('E4', 0.5), ('D4', 1), ('G4', 1),
  
]



def setCouleur(couleur):
    for i in range(LEN_LED):
        strip.setPixelColor(i, couleur)
        strip.show()


def music_led():
    for note, duration in melody:
            note_couleur = note_couleurs.get(note, 0)

            print(note_couleur)
            if note_couleur:
                setCouleur(note_couleur)
            play_light(note_couleur, duration)
            led_close()
            time.sleep(1.0 / 15)  
        
    time.sleep(1)

def start():
    
    
    
    
    strip.show()
    while True:
        

        
        for note, duration in melody:
            note_couleur = note_couleurs.get(note, 0)

            print(note_couleur)
            if note_couleur:
                setCouleur(note_couleur)
            play_light(note_couleur, duration)
            led_close()
            time.sleep(1.0 / 15)  
        
        time.sleep(1)
start()
