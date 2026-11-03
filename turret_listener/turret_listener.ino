// Serial listener for the face-tracking turret.
// Receives pan angles from sentry_turret.py as "P<angle>\n" at 9600 baud
// and drives the pan servo on pin 6.
#include <Servo.h>

Servo panServo;

void setup() {
  Serial.begin(9600);
  panServo.attach(6);
  panServo.write(90);  // center on boot
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command.startsWith("P")) {
      int targetAngle = command.substring(1).toInt();
      targetAngle = constrain(targetAngle, 10, 170);  // stay inside servo limits
      panServo.write(targetAngle);
    }
  }
}
