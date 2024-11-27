import pigpio
import time
from rpi_ws281x import PixelStrip, Color

# Configuration des LEDs
LENLED = 50
LED_PIN = 12  # GPIO 12 pour les LEDs
strip = PixelStrip(LENLED, LED_PIN)
strip.begin()  # Assurez-vous que le strip commence correctement
strip.setBrightness(100)  # Réglez la luminosité des LEDs (entre 0 et 255)

# Configuration du buzzer
pi = pigpio.pi()
BUZZER_PIN = 18  # GPIO 18 pour le buzzer
pi.set_mode(BUZZER_PIN, pigpio.OUTPUT)

# Fréquences des notes
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

# Mélodie de "We Wish You a Merry Christmas"
melody = [
    ('B3', 0.4), ('E4', 0.4), ('E4', 0.4), ('F4', 0.4), ('E4', 0.4), ('D4', 0.4), ('C4', 0.4),
    ('C4', 0.4), ('D4', 0.4), ('E4', 0.4), ('A4', 0.4), ('G4', 0.4), ('G4', 0.6),
    ('C4', 0.4), ('E4', 0.4), ('E4', 0.4), ('F4', 0.4), ('E4', 0.4), ('D4', 0.4), ('C4', 0.4),
    ('A4', 0.4), ('C5', 0.4), ('B4', 0.4), ('G4', 0.4), ('A4', 0.8)
]

# Fonction pour jouer une note
def play_tone(pin, frequency, duration):
    if frequency == 0:
        time.sleep(duration)
        return
    pi.hardware_PWM(pin, frequency, 500000)  # PWM pour le buzzer
    time.sleep(duration)
    pi.hardware_PWM(pin, 0, 0)  # Arrêt du PWM

# Fonction pour changer la couleur des LEDs
def change_color(color):
    print(f"Changing color to {color}")
    for i in range(LENLED):
        strip.setPixelColor(i, color)
    strip.show()  # Actualisation des LEDs

# Test des LEDs (toutes en rouge)
def test_leds():
    print("Test des LEDs - Toutes les LEDs devraient être rouges")
    for i in range(LENLED):
        strip.setPixelColor(i, Color(255, 0, 0))  # Allumer chaque LED en rouge
    strip.show()  # Mettre à jour les LEDs

# Jouer la mélodie et changer les couleurs des LEDs
try:
    print("Starting the test...")

    # Liste des couleurs à alterner : Rouge, Vert, Bleu
    colors = [Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255)]  # Rouge, vert, bleu
    color_index = 0  # Index pour alterner les couleurs

    print("Playing 'We Wish You a Merry Christmas'...")

    for note, duration in melody:

        # Changer la couleur des LEDs
        change_color(colors[color_index])
        color_index = (color_index + 1) % 3  # Alterner les couleurs (0 -> 1 -> 2 -> 0)

        frequency = notes.get(note, 0)

        # Jouer la note sur le buzzer
        play_tone(BUZZER_PIN, frequency, duration)

        time.sleep(0.1)  # Pause entre les notes

    print("Done!")
except KeyboardInterrupt:
    print("Interrupted!")
    pi.write(BUZZER_PIN, 0)  # Arrêter le buzzer
    change_color(Color(0, 0, 0))  # Éteindre les LEDs
finally:
    pi.stop()  # Arrêter la connexion pigpio
