## Files
- <b>abhiraj_balldet.py</b>: using color detection, hough circles, elimination using centroid matching.
 <br> **Errors** <br>
 1. Detects a roundish bottle as ball. *Reason -* Hough circles. *Solution -* use centroid of contour to eliminate.
 2. Does not work in sunlight. *Reason -* overexposure of ball. *(Unsolved)*
---
- <b>abhiraj_obstacle_avoidance.py</b>: using ultrasonic sensors.
 <br> **Errors** <br>
 Did not work outdoors *Reason -* long timout. *Solution -* implement manual timeout.
---
- <b>dataset.zip</b>: dataset of ball and no ball.
---
- <b>joy on uart.py</b>: joystick sends the pwm values to a companion arduino program *(uart_motor_reciever)* 
 <br> **Errors** <br>
 The data being sent by raspberry pi, was not being recieved correctly by the arduino. *Solution -* added start and stop bytes to the data packet
---
- <b>multicam.py</b>: using multiple cameras connected to the usb port, using multithreading to reduce lag
 <br> **Errors** <br>
 Unable to cleanup the threads after the program ends. 
 Shitty error handling where the program hangs, if there is an error in either of the threads.
---
- <b>mypwm.py</b>: trying to implement software pwm on the raspberry pi's pins.
 <br> **Errors** <br>
 Can't use with programs where there are delays
---
- <b>pwmjoy.py</b>: trying to implement software pwm, joystick code, using mypwm.py 
 <br> **Errors** <br>
 *possibly* the code takes too much time to loop which hinders the working of the mypwm softpwm pins. RPi.GPIO's pwm is based on multithreading. maybe that is the solution for this.
---
- <b>pwmjoy_lib.py</b>: joystick code with software pwm on raspberry pi using RPi.GPIO library
---
- <b>usbjoystick.py</b>: simple joystick program


