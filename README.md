# Arduino_Ball_Sorter
Robotics (RBT200) Ball sorter project. 

Files:

pygameCamera.py - the python code that will be used on the raspberry pi. Contains code for the camera and writing serial commands to the arduino. Prerequisites: PyGame 1.9.1, python 2.7.x

ball_sorter.ino - the arduino code for the ball sorter. Contains code that converts serial messages to servo movement and co-ordinates two servos. We used an Arduino Mega.

notes.h - piezo note definition module. 

lcd_screen_test.ino - prototype sketch for the LCD screen with working serial input and counting functions. Not used in final program.

Plan/Documentation of code (particularly Python code) is defined here:
https://docs.google.com/presentation/d/1EglKOPJg7bWesM6bb773WEh6BpbUDmNyZhsR3al7E0Y/edit?usp=sharing


To do list and development is now kept in ISSUES section
