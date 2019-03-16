import pygame
import serial

pygame.init()
pygame.joystick.init()

joy = pygame.joystick.Joystick(0)
joy.init()

ser = serial.Serial('/dev/ttyUSB0', 38400)


try:
    x_joy = 0
    y_joy = 0
    x_joy_last = 0
    y_joy_last = 0
    addx = 512
    addy = 512
    while True:
        x_joy = x_joy_last 
        y_joy = y_joy_last
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    x_joy = event.value*512 #-255 because the joystick was reverse mapped
                elif event.axis == 1:
                    y_joy = event.value*-512

        x_joy_last = x_joy
        y_joy_last = y_joy

        x_joy = int(x_joy)
        y_joy = int(y_joy)
        x_joy = x_joy + addx
        y_joy = y_joy + addy
        x_joy = max(min(1023, x_joy), 0)
        y_joy = max(min(1023, y_joy), 0)
        print x_joy, y_joy

        # sending x
        tenbit2 = x_joy >> 5
        tenbit2 |= 0b11000000
        ser.write(chr(tenbit2))

        tenbit1 = x_joy & 0b00011111
        tenbit1 |= 0b10000000
        ser.write(chr(tenbit1))

        # sending y
        tenbit4 = y_joy >> 5
        tenbit4 |= 0b00000000
        ser.write(chr(tenbit4))

        tenbit3 = y_joy & 0b00011111
        tenbit3 |= 0b01000000
        ser.write(chr(tenbit3))
        # print '{0:b}'.format(tenbit2), '{0:b}'.format(tenbit1), '{0:b}'.format(tenbit4), '{0:b}'.format(tenbit3)

except KeyboardInterrupt:
    pass

pygame.quit()
