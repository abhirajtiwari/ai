import pygame
import serial

pygame.init()
pygame.joystick.init()

ser = serial.Serial('/dev/ttyACM0', 115200)

joy = pygame.joystick.Joystick(0)
joy.init()

try:
    x_joy = 0
    y_joy = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    x_joy = event.value*512 #-255 because the joystick was reverse mapped
                elif event.axis == 1:
                    y_joy = event.value*-512


        # lpwm = x_joy+y_joy
        # rpwm = y_joy-x_joy
        # lpwm = int(max(min(255, lpwm), -255))
        # rpwm = int(max(min(255, rpwm), -255))
        # ldir = 'f' if lpwm >= 0 else 'b'
        # rdir = 'f' if rpwm >= 0 else 'b'

        x_joy += 512
        y_joy += 512
        x_joy = int(x_joy)
        y_joy = int(y_joy)

        # sending x
        tenbit2 = x_joy >> 5
        tenbit2 |= 0b11000000
        ser.write(chr(tenbit2))

        tenbit1 = x_joy & 0b00011111
        tenbit1 |= 0b00000000
        ser.write(chr(tenbit1))

        # sending y
        tenbit4 = (y_joy>>5);
        tenbit4 |= 0b00000000;
        ser.write(chr(tenbit4))
        
        tenbit3 = y_joy & 0b00011111;
        tenbit3 |= 0b01000000;
        ser.write(chr(tenbit3))

except KeyboardInterrupt:
    pass

finally:
    pygame.quit()
