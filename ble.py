import time
import pigpio
 
BTN = 27
 
# Init GPIO
pi = pigpio.pi()
cur = pi.read(BTN)
last = cur
compteur = 0
count = 0
isPressed = False
isAllume = True
 
 
def mode1():
    print('mode1')
 
 
def mode2():
    print('mode2')
        
 
 
 
if __name__ == '__main__':
    try:
        while True:
            cur = pi.read(BTN)
            print(cur)
            if(not isPressed):
                if(cur == 1):
                    count = 0
                elif(count < 4):
                    count += 1
                elif(count == 4):
                    compteur +=1
                    count = 0
                    if compteur%2 != 0:
                        mode2()
                    else:
                        mode1()
                    isPressed = True
            else:
                if(cur == 0):
                    count = 0
                elif(count < 4):
                    count += 1
                elif(count == 4):
                    count +=1
                    isPressed = False
            
            last = cur
    except KeyboardInterrupt:
        print("\nJoyeux NAEL!!!")