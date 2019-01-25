import pygame

pygame.init()
pygame.joystick.init()

joy = pygame.joystick.Joystick(0)
joy.init()

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    x_joy = event.value*255 #-255 because the joystick was reverse mapped
                elif event.axis == 1:
                    y_joy = event.value*-255
        # print x_joy, y_joy
        lpwm = x_joy+y_joy
        rpwm = y_joy-x_joy
        lpwm = max(min(255, lpwm), -255)
        rpwm = max(min(255, rpwm), -255)
        print lpwm, rpwm

except KeyboardInterrupt:
    pass

pygame.quit()
