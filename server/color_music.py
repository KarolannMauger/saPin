from rpi_ws281x import PixelStrip, Color
import time

LEN_LED = 50

strip = PixelStrip(LEN_LED, 12)
strip.begin()
strip.setBrightness(255)  # Assurez-vous que la luminosité est maximale

# https://www.seventhstring.com/resources/notefrequencies.html
note_couleur = {
   'E4': Color(255, 0, 0),
   'G4': Color(0, 255, 0),
   'C4': Color(0, 0, 255),
   'D4': Color(255, 255, 0),
   'F4': Color(0, 255, 255),
   'Silence': 'Silence'
}

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

def start():
    while True:
        for note, duration in melody:
            couleur = note_couleur.get(note, 0)
            print(f"Note: {note}, Couleur: {couleur}")
            if couleur != 'Silence':
                setCouleur(couleur)
            else:
                strip.setBrightness(0)
                strip.show()
            time.sleep(duration)
        time.sleep(1)

start()
