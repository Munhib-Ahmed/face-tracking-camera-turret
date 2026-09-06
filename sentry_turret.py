import cv2
import serial
import time
import numpy as np

# 1. Connect to the Arduino Mega
try:
    # CHANGE 'COM3' TO YOUR ACTUAL ARDUINO PORT
    arduino = serial.Serial('COM3', 9600, timeout=1) 
    time.sleep(2) # Give the Mega a second to reboot
    print("Mega Connected.")
except Exception as e:
    print(f"Failed to connect: {e}")
    exit()

# 2. Load OpenCV's built-in face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 3. Start the USB Webcam
cap = cv2.VideoCapture(1)
current_pan = 90
KP = 0.035 # Increased for sharper tracking (Goldilocks zone)

while True:
    ret, frame = cap.read()
    if not ret: break

    # Flip horizontally so it acts like a mirror
    frame = cv2.flip(frame, 1)
    frame_h, frame_w, _ = frame.shape
    center_x = frame_w // 2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        # Grab the first face it sees
        (x, y, w, h) = faces[0]
        face_center_x = x + w // 2

        # Draw a box around your face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate how far off-center your face is
        error_x = face_center_x - center_x

        # Tightened the deadzone to 15 pixels so it reacts sooner
        if abs(error_x) > 15:
            # Calculate new servo angle
            current_pan += error_x * KP 
            current_pan = np.clip(current_pan, 10, 170)

            # Send to Arduino
            arduino.write(f"P{int(current_pan)}\n".encode())

    # Show the video feed
    cv2.imshow('1-Axis Sentry Turret', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()