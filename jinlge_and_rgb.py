import pigpio
import time


pi = pigpio.pi()


BUZZER_PIN = 18
RED_PIN = 17   
GREEN_PIN = 27 
BLUE_PIN = 22  

pi.set_mode(BUZZER_PIN, pigpio.OUTPUT)
pi.set_mode(RED_PIN, pigpio.OUTPUT)
pi.set_mode(GREEN_PIN, pigpio.OUTPUT)
pi.set_mode(BLUE_PIN, pigpio.OUTPUT)

##https://www.seventhstring.com/resources/notefrequencies.html
notes = {
   'E4': 329,
   'G4': 392,
   'C4': 261,
   'D4': 293,
   'F4': 349,
   'Silence': 0
}


colors = [
    (1, 0, 0),  
    (0, 1, 0),  
    (0, 0, 1), 
    (1, 1, 0),  
    (0, 1, 1), 
    (1, 0, 1)  
]

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

def set_rgb_color(red, green, blue):
    pi.write(RED_PIN, red)
    pi.write(GREEN_PIN, green)
    pi.write(BLUE_PIN, blue)

try:
    print("Playing 'Jingle Bells'...")

    color_index = 0

    for note, duration in melody:
        frequency = notes.get(note, 0)

        
        red, green, blue = colors[color_index]
        set_rgb_color(red, green, blue)

       
        play_tone(BUZZER_PIN, frequency, duration)

        
        time.sleep(1.0 / 15)

        
        color_index = (color_index + 1) % len(colors)

    print("Done!")

except KeyboardInterrupt:
    print("Interrupted!")
    pi.write(BUZZER_PIN, 0)
    pi.write(RED_PIN, 1)
    pi.write(GREEN_PIN, 1)
    pi.write(BLUE_PIN, 1)

finally:
    pi.stop()
