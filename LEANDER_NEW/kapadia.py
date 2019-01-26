import pygame
from pygame import locals

speedA =0.000
speedB =0.000

x=512.00
y=512.00

def arduino_map(x, in_min, in_max, out_min, out_max):
  return ((x - in_min) * (out_max - out_min) / (in_max - in_min)) + out_min

def oct1(x,y):
    speedA = arduino_map(y,1023,512,255,0)
    speedB = arduino_map(x+y,1535,1023,255,0)
    print("leftF=",speedA)
    print("rightF=",speedB)

def oct2(x,y):
    speedA = arduino_map(x,512,0,0,255)
    speedB = arduino_map(x+y,1023,512,0,255)
    print("leftF=",speedA)
    print("rightB=",speedB)

def oct3(x,y):
    speedA = arduino_map(y-x,512,0,255,0)
    speedB = arduino_map(x,512,0,0,255)
    print("leftF=",speedA)
    print("rightB=",speedB)

def oct4(x,y):
    speedA = arduino_map(x-y,512,0,255,0)
    speedB = arduino_map(y,512,0,0,255)
    print("leftB=",speedA)
    print("rightB=",speedB)

def oct5(x,y):
    speedA = arduino_map(y,512,0,0,255)
    speedB = arduino_map(x+y,1023,512,0,255)
    print("leftB=",speedA)
    print("rightB=",speedB)

def oct6(x,y):
    speedA = arduino_map(x,1023,512,255,0)
    speedB = arduino_map(x+y,1535,1023,255,0)
    print("leftB=",speedA)
    print("rightF=",speedB)

def oct7(x,y):
    speedA = arduino_map(x-y,0,512,0,255)
    speedB = arduino_map(x,1023,512,255,0)
    print("leftB=",speedA)
    print("rightF=",speedB)

def oct8(x,y):
    speedA = arduino_map(y-x,0,512,0,255)
    speedB = arduino_map(y,1023,512,255,0)
    print("leftF=",speedA)
    print("rightF=",speedB)


pygame.init()
pygame.joystick.init() # main joystick device system

try:
	j = pygame.joystick.Joystick(0) # create a joystick instance
	j.init() # init instance
	print ("Enabled joystick:")
except pygame.error:
	print ("no joystick found.")

while 1:
	for e in pygame.event.get(): # iterate over event stack
                if e.type == pygame.locals.JOYAXISMOTION:
                    x ,y =  j.get_axis(0) ,j.get_axis(1)
                    x=arduino_map(x, -1, 1, 0, 1024)
                    y=arduino_map(y, -1, 1, 0, 1024)
                    print("X=",x)
                    print("Y=",y)

                    #QUAD 1
                    if (x <= 512) &  ((y >= 512) &  (y <= 1023)):

                        if (x + y) >= 1023: # OCT1
                            oct1(x, y)

                        if (x + y) < 1023: #OCT2
                            oct2(x, y)

                    #QUAD 2
                    if (x <= 512) &  (y <= 512):

                        if (x - y) <= 0: # OCT3
                            oct3(x, y)

                        if (x - y) > 0: # OCT4
                            oct4(x, y)



                    #QUAD 3
                    if ((x >= 512)  & (x <= 1023))  & (y <= 512):


                        if (x + y) <= 1023: # OCT5
                            oct5(x, y)

                        if (x + y) > 1023: # OCT6
                            oct6(x, y)



                    #QUAD 4
                    if ((x >= 512)  & (x <= 1023)) & ((y >= 512) & (y <= 1023)):

                        if (y - x) <= 0: # OCT7
                            oct7(x, y)

                        if (y - x) > 0:  # OCT8
                            oct8(x, y)

