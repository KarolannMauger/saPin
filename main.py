import time
import pigpio
import TEMT6000_sensor
import music_script
from threading import Thread

BTN = 27

pi = pigpio.pi()
cur = pi.read(BTN)

last = cur
compteur = 1
count = 0
isPressed = False


sensor_thread = None
music_thread = None


stop_sensor_thread = False
stop_music_thread = False



def stop_sensor():
    global stop_sensor_thread
    stop_sensor_thread = True

def restart_sensor_thread():
    global sensor_thread, stop_sensor_thread
    stop_sensor_thread = False
    if sensor_thread is not None and sensor_thread.is_alive():
        print("Arrêt du thread capteur précédent.")
        stop_sensor()
        sensor_thread.join()
    sensor_thread = Thread(target=TEMT6000_sensor.start, args=(lambda: stop_sensor_thread,))
    sensor_thread.start()


def stop_music():
    global stop_music_thread
    stop_music_thread = True

def restart_music_thread():
    global music_thread, stop_music_thread
    stop_music_thread = False
    if music_thread is not None and music_thread.is_alive():
        print("Arrêt du thread musique précédent.")
        stop_music()
        music_thread.join()
    music_thread = Thread(target=music_script.play_music, args=(lambda: stop_music_thread,))
    music_thread.start()


def mode1():
    print('Mode 1 activé')
    stop_sensor()
    restart_music_thread()

def mode2():
    print('Mode 2 activé')
    stop_music()
    restart_sensor_thread()


if __name__ == '__main__':
    try:
        mode2()
        while True:
            cur = pi.read(BTN)

            if not isPressed:
                if cur == 1:
                    count = 0
                elif count < 4:
                    count += 1
                elif count == 4:
                    compteur += 1
                    count = 0
                    if compteur % 2 != 0:
                        mode2()
                    else:
                        mode1()
                    isPressed = True
            else:
                if cur == 0:
                    count = 0
                elif count < 4:
                    count += 1
                elif count == 4:
                    count += 1
                    isPressed = False
            
            last = cur
    except KeyboardInterrupt:
        print("\nJOYEUX NAEL")
        stop_sensor()
        stop_music()
