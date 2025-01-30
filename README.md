## SaPin 🎄
**SaPin** is an interactive and festive project based on two Raspberry Pi devices, designed to capture the spirit of Christmas through lights, music, and animations. It combines technology and creativity to create a magical and immersive experience.

---

## Features
- 🎅 **Two operating modes:**  
  - **Mode 1:** Lights always on, music (*Jingle Bells*) played through a buzzer, and a sparkling animation on an 8x8 LED matrix.
   -🎵 **New! Music and lights are now synchronized for a more immersive experience!** 
  - **Mode 2:** Lights and the servo motor activate only in the dark, thanks to a light sensor.

- ✨ **Animated decoration:** A servo motor moves a festive decoration.

- 💡 **WS2811 addressable LED string:** LED lights controlled independently through a TCP connection.

- 🔌 **TCP connection:** Communication between two Raspberry Pi devices for distributed management of features.

---

## Required Materials

- **2 Raspberry Pi devices** (one server, one client)
- **Digital Push Button Keystudio**
- **Keystudio Photocell Sensor** with **ADS1115 module**
- **Keystudio Passive Buzzer**
- **WS2811 Digital LED String** (50 LEDs)
- **Micro Servo 9G**
- **Keystudio 8x8 LED Matrix (KS0522)**
- **External power supply** for the LED string

---

## Installation
### Sofware Dependencies
**Before the installation you need to :**
  ```bash
  $ sudo apt update -y
  $ sudo apt upgrade -y
  ```
**Instruction will be available soon for i2c device**
Client : Library adafruit-circuitpython-ht16k33
  ```bash
   $ pip3 install adafruit-circuitpython-ht16k33 --break-system-packages
  ```
Server : Library rpi_ws281x
  ```bash
   $ sudo apt install python3-pip python3-dev build-essential
   $ sudo pip3 install rpi_ws281x
  ```

⚠️ **Note**: The rpi_ws281x library conflicts with pigpio. 
To resolve this, LED string management is handled by a separate Raspberry Pi via a TCP connection.

### GPIO Connections

#### Client Raspberry Pi

| GPIO Pin  | Component                          | Description            |
|-----------|-------------------------------------|------------------------|
| GPIO 17   | Servo motor                        | Movement control       |
| GPIO 18   | Passive buzzer                     | Music playback         |
| GPIO 27   | Push button                        | Mode switching         |
| SDA/SCL   | 8x8 LED matrix and ADS1115         | I²C communication      |
| ADS1115   | Photocell sensor                   | Light intensity measurement |

#### Server Raspberry Pi

| GPIO Pin  | Component                          | Description            |
|-----------|-------------------------------------|------------------------|
| GPIO 12   | WS2811 LED string                  | Light control          |

---

## Usage

### Step 1: Start the TCP Server
On the Raspberry Pi controlling the LED string, run the server script:
```bash
$ python3 tcp_serveur.py
```

### Step2: Start the Client
On the second Raspberry Pi, run the client script:
```bash
$ python3 main.py
```

### Step 3: Switch Between Modes
- **Mode 2 (default):** Automatically activates in the dark. The lights and servo motor will only work when the photocell sensor detects low light.
- **Mode 1:** Press the button to activate all features, including:
  - Constantly lit lights
  - **Music playback (*Jingle Bells*), now synchronized with the LED lights**
  - Sparkling animation on the 8x8 LED matrix

### Step 4: Stop the Program
To stop the program:
1. Stop the client script:
   ```bash
   Ctrl+C
   ```
2. Then stop the server script:
   ```bash
   Ctrl+C
   ```

---

## References
- ht16k33 Library (8x8 LED matrix): [Adafruit HT16K33 Matrix8x8 API](https://docs.circuitpython.org/projects/ht16k33/en/latest/api.html#adafruit_ht16k33.matrix.Matrix8x8)
- WS281 Library (LED string): [rpi-ws281x-python GitHub](https://github.com/rpi-ws281x/rpi-ws281x-python/tree/master)
- Musical note frquencies: [Musical note frequencies](https://www.seventhstring.com/resources/notefrequencies.html)
- Jingle bell: [Jingle bell - Beginner version](https://pianognu.blogspot.com/2015/08/vive-le-vent-version-debutant.html)
- Python Threads Tutorial: [Multithreading in Python - Set 1](https://www.geeksforgeeks.org/multithreading-python-set-1/)

---

## Demo
🎥 **Watch SaPin in action!** Now with **music synchronized with the LED lights**!
### 🌟 Latest Version - Music & Lights Sync
[![SaPin Demo (Updated)](https://img.youtube.com/vi/eMOymc6_Dm0/0.jpg)](https://www.youtube.com/watch?v=eMOymc6_Dm0)
🎶 In this updated version, the LED lights are now synchronized with the music in Mode 1 for an even more immersive experience.
---
### 🎬 Original Version
[![SaPin Demo (Original)](https://img.youtube.com/vi/eMOymc6_Dm0/0.jpg)](https://www.youtube.com/watch?v=eMOymc6_Dm0)
🔔 This was the first version of SaPin before the music0light synchronization update. It's still available if you want to see how the project evolved!

---

## Author
- :floppy_disk: [@Loulouplou](https://www.github.com/Loulouplou)
- :floppy_disk: [@KarolannMauger](https://www.github.com/KarolannMauger)

---

## License  
This project is developed as part of the course *PROGRAMMATION DE PLATEFORMES EMBARQUÉES | 420-314-MV*.  
Copyright © [2024] [@Loulouplou](https://www.github.com/Loulouplou) and [@KarolannMauger](https://www.github.com/KarolannMauger).  
All rights reserved. Redistribution, modification, and commercial use are strictly prohibited.  

---

🎅 *Happy holidays from the saPin team!*
