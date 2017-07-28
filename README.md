# Arduino-OpenCV-Human-Follower

![robot](https://cloud.githubusercontent.com/assets/8938083/9835888/d5c6283c-5a1d-11e5-9fff-320f656139b1.jpg)

1. [Dependencies](#dependencies)
2. [Hardware](#hardware)
3. [Setup and Algorithm](#setup-and-algorithm)

## Dependencies
* PySerial
* OpenCV for Python

## Hardware
* Arduino Uno
* Chassis
* webcam
* motor driver

The assembled chassis with webcam looks like this.
![chassis](https://cloud.githubusercontent.com/assets/8938083/9835869/6735cc6a-5a1d-11e5-9143-474a5d0ea821.jpg)

## Setup and Algorithm
The project uses OpenCV library with python for building an algorithm to detect humans by tracking faces. The hardware is based on Arduino microcontroller and an external webcam connected via an intermediate personal computer where all the image processing takes place. Both the Arduino and the webcam are mounted on a chassis.

Based on the position and size of the face detected, signals from the computer are serially communicated to the Arduino which in turn controls the bot to move accordingly to keep tracking the human face.
