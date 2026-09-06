# OpenCV Face-Tracking Sentry Turret

![Turret Action Demo](sentry-gif.gif) 


## Overview
A single-axis face-tracking sentry turret driven by proportional control. The system uses a USB webcam and OpenCV's Haar Cascades to detect a face, calculates the pixel offset from the center of the frame, and sends serial commands to an Arduino Mega to actuate a pan servo. 

## Hardware Stack
*   **Microcontroller:** Arduino Mega 2560
*   **Vision:** Standard USB Webcam
*   **Actuation:** Standard 5V Servo Motor
*   **Chassis:** Custom 3D-printed mounting brackets and hardware

## Software Dependencies
*   Python 3.x
*   `opencv-python`
*   `pyserial`
*   `numpy`

## Control Logic
The tracking utilizes a proportional control loop (Kp = 0.035). The Python script calculates the horizontal error (`error_x`) between the target face center and the camera frame center. To prevent mechanical jitter and micro-stutters, a 15-pixel deadzone is implemented. If the target leaves the deadzone, the script calculates a new pan angle clamped between 10° and 170° and writes the coordinate to the Arduino over Serial.

## Installation & Setup

1. **Wire the Hardware:** 
   * Connect the servo signal pin to the Arduino Mega. Provide external 5V power to the servo to avoid burning out the Mega's voltage regulator.
   * *(Note: Insert a photo of your wiring setup here)*

2. **Flash the Arduino:**
   * Upload a standard servo control sketch to the Arduino Mega that listens to the Serial monitor at `9600` baud, reads the incoming integer (prefixed by 'P'), and writes it to the servo. 

3. **Install Python Libraries:**
   ```bash
   pip install opencv-python pyserial numpy