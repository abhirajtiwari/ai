import pygame


pygame.init()
pygame.joystick.init()

joyStick = pygame.joystick.Joystick(0)
joyStick.init()

x_value = 0.00
y_value = 0.00

while True:
    for event in pygame.event.get():
        if(event.type == pygame.JOYAXISMOTION):
            if(event.axis==0):
                x_value = joyStick.get_axis(0)  #gets the position of the joystick on x axis
            elif(event.axis==1):
                y_value = -joyStick.get_axis(1)

        else:
            print('not on the axis')


        print('x_value',x_value)
        print('y_value',y_value)


    	if(x_value == 0 and y_value ==0):
	    print('center')


    #quad 1
        if(x_value > 0 and y_value > 0):
            if(x_value - y_value < 0):
                print('oct 1')
            else:
                print('oct 2')
    #quad 3
        if(x_value < 0 and y_value < 0):
            if(x_value - y_value < 0):
                print('oct 5')
            else:
                print('oct 6')
    #quad 2
        if(x_value < 0 and y_value > 0):
            if(x_value + y_value > 0):
                print('oct 3')
            else:
                print('oct 4')
    #quad 4
        if(x_value > 0 and y_value < 0):
            if(x_value + y_value > 0):
                print('oct 8')
            else:
                print('oct 7')



print('not on any axis')
