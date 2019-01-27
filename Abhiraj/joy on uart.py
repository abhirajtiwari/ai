import pygame
import serial

pygame.init()
pygame.joystick.init()

ser = serial.Serial('/dev/serial0', 115200)

joy = pygame.joystick.Joystick(0)
joy.init()

try:
    x_joy = 0
    y_joy = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    x_joy = event.value*255 #-255 because the joystick was reverse mapped
                elif event.axis == 1:
                    y_joy = event.value*-255
        lpwm = x_joy+y_joy
        rpwm = y_joy-x_joy
        lpwm = int(max(min(255, lpwm), -255))
        rpwm = int(max(min(255, rpwm), -255))
        ldir = 'f' if lpwm >= 0 else 'b'
        rdir = 'f' if rpwm >= 0 else 'b'
        packet = 's' + ldir + str(format(abs(lpwm), '03')) + rdir + str(format(abs(rpwm), '03')) + 'e'
        ser.write(packet.encode('utf-8'))
        print packet

except KeyboardInterrupt:
    pass

finally:
    pygame.quit()
