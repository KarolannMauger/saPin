# SaPin 🎄
**SaPin** is an interactive and festive project based on two Raspberry Pi devices, designed to capture the spirit of Christmas through lights, music, and animations. It combines technology and creativity to create a magical and immersive experience.

---

## Features
- 🎅 **Two operating modes:**  
  - **Mode 1:** Lights always on, music (*Jingle Bells*) played through a buzzer, and a sparkling animation on an 8x8 LED matrix.  
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
**Instructions will be available soon.**
Client : Library adafruit-circuitpython-ht16k33
Server : Library rpi_ws281x

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
  - Music playback (*Jingle Bells*)
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
- ht16k33 Library (8x8 LED matric): Official documentation will be added soon.
- WS281 Library (LED string): Will be added soon.
- Musical note frquencies: Will be added soon.
- Python Threads Tutorial: Will be added soon.

---

## Demo
The demo will be added soon


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
