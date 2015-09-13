# Arduino-OpenCV-Face-Follower

The project uses OpenCV library with python for building an algorithm to detect humans by tracking faces.
The hardware is based on Arduino microcontroller and an external webcam connected via an intermediate personal computer where all the image processing takes place.
Both the Arduino and the webcam are mounted on a chassis.
Based on the position and size of the face detected, signals from the computer are serially communicated to the Arduino which in turn controls the bot to move accordingly to keep tracking the human face.

Dependencies: PySerial, OpenCV
Hardware: Arduino Uno, Chassis, webcam
