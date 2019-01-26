import pygame


pygame.init()
pygame.joystick.init()

joyStick = pygame.joystick.Joystick(0)
joyStick.init()

x_value = 0.00
y_value = 0.00


def oct1():
    led_left_fwd = x_pwm
    led_right_bck = 255 - y_pwm
    print(x_pwm)
    print(255-y_pwm)

def oct2():
    led_left_fwd = y_pwm
    led_right_bck = y_pwm - x_pwm
    print(y_pwm)
    print(y_pwm - x_pwm)

def oct3():
    led_left_fwd = y_pwm - x_pwm
    led_right_bck = y_pwm
    print(y_pwm - x_pwm)
    print(y_pwm)

def oct4():
    led_left_fwd = x_pwm - y_pwm
    led_right_bck = x_pwm
    print(x_pwm - y_pwm)
    print(x_pwm)

def oct5():
    led_left_fwd = x_pwm
    led_right_bck = x_pwm - y_pwm
    print(x_pwm)
    print(x_pwm - y_pwm)

def oct6():
    led_left_fwd = y_pwm
    led_right_bck = y_pwm - x_pwm
    print(y_pwm)
    print(y_pwm - x_pwm)

def oct7():
    led_left_fwd = y_pwm - x_pwm
    led_right_bck = y_pwm
    print(y_pwm - x_pwm)
    print(y_pwm)

def oct8():
    led_left_fwd = x_pwm - y_pwm
    led_right_bck = x_pwm
    print(x_pwm - y_pwm)
    print(x_pwm)

while True:
    for event in pygame.event.get():
        if(event.type == pygame.JOYAXISMOTION):
            if(event.axis==0):
                x_value = joyStick.get_axis(0)  #gets the position of the joystick on x axis
            elif(event.axis==1):
                y_value = -joyStick.get_axis(1)

        else:
            print('not on the axis')

        x_pwm = abs(round(x_value * 255))
        y_pwm = abs(round(y_value * 255))
        #print('x_value', x_pwm)
        #print('y_value', y_pwm)


    	if(x_value == 0 and y_value ==0):
	    print('center')


    #quad 1
        if(x_value > 0 and y_value > 0):
            if(x_value - y_value > 0):
                print('oct 1')
                oct1()
            else:
                print('oct 2')
                oct2()
    #quad 3
        if(x_value < 0 and y_value < 0):
            if(x_value - y_value < 0):
                print('oct 5')
                oct5()
            else:
                print('oct 6')
                oct6()
    #quad 2
        if(x_value < 0 and y_value > 0):
            if(x_value + y_value > 0):
                print('oct 3')
                oct3()
            else:
                print('oct 4')
                oct4()
    #quad 4
        if(x_value > 0 and y_value < 0):
            if(x_value + y_value > 0):
                print('oct 8')
                oct8()
            else:
                print('oct 7')
                oct7()


print('not on any axis')
