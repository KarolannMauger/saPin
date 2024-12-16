import time
import pigpio
import staranim
import jinglebell
import snot2
from threading import Thread

# Initialisation de la connexion pigpio
pi = pigpio.pi()
BTN = 27  # Pin pour le bouton
pi.set_mode(BTN, pigpio.INPUT)
pi.set_pull_up_down(BTN, pigpio.PUD_UP)

BUZZER_PIN = 18
pi.set_mode(BUZZER_PIN, pigpio.OUTPUT)

# Variables de gestion du bouton et du mode
cur = pi.read(BTN)
last = cur
count = 0
compteur = 0
isPressed = False

# Variables pour les threads
principal_thread = None  # Pour gérer le thread principal
stop_principal_thread = False  # Contrôle pour arrêter le thread principal

# Fonction pour arrêter le thread principal
def stop_sensor():
    global stop_principal_thread
    stop_principal_thread = True
    if principal_thread is not None and principal_thread.is_alive():
        stop_principal_thread = True
        principal_thread.join()  # Attendre que le thread se termine

# Fonction pour redémarrer un thread d'animation
def restart_toto(target_name):
    global principal_thread, stop_principal_thread
    stop_principal_thread = False  # Réinitialise l'arrêt
    if principal_thread is not None and principal_thread.is_alive():
        stop_sensor()  # Arrête le thread actuel
    principal_thread = Thread(target=target_name, args=(lambda: stop_principal_thread,))
    principal_thread.start()

# Fonction pour gérer le mode1 (musique + animation)
def mode1():
    print('mode1')
    stop_sensor()  # Assure que l'animation est stoppée
    restart_toto(jinglebell.start)  # Redémarre le mode jinglebell

# Fonction pour gérer le mode2 (animation seulement)
def mode2():
    print('mode2')
    stop_sensor()  # Assure que l'animation est stoppée
    restart_toto(snot2.toto)  # Redémarre le mode snot2

# Fonction principale pour surveiller le bouton
if __name__ == '__main__':
    try:
        mode2()  # On démarre en mode2
        while True:
            cur = pi.read(BTN)

            # Logique de gestion du bouton pour changer de mode
            if not isPressed:
                if cur == 1:  # Si le bouton est relâché, on réinitialise le compteur
                    count = 0
                elif count < 4:  # On attend les 4 clics avant de changer de mode
                    count += 1
                elif count == 4:  # Lorsque le bouton a été pressé 4 fois
                    count = 0  # Réinitialiser le compteur pour le prochain appui
                    if compteur % 2 != 0:  
                        print("Changement vers mode2")
                        stop_sensor()  # Arrêter l'animation en cours
                        mode2()  # Passer en mode2
                    else:  
                        print("Changement vers mode1")
                        stop_sensor()  # Arrêter l'animation en cours
                        mode1()  # Passer en mode1
                    compteur += 1  # Incrémenter le compteur pour alterner les modes
                    isPressed = True  # Marquer le bouton comme pressé

            # Lorsque le bouton est relâché, réinitialiser l'état "pressé"
            if cur == 0:  # Le bouton est appuyé
                isPressed = False

            last = cur  # Mettre à jour l'état précédent du bouton

    except KeyboardInterrupt:
        print("\nJoyeux NAEL!!!")
