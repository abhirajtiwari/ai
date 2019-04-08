import pygame
import subprocess
import serial
import time
import threading

print 'Joystick with ATmega'

pygame.init()
pygame.joystick.init()

joy = pygame.joystick.Joystick(0)
joy.init()

#Udit's baudrate 38400
ser = serial.Serial('/dev/ttyUSB0', 38400)
check_running = True
numgears = 4
x_joy = 0
y_joy = 0
gear= 0
x_joy_last = 512
y_joy_last = 512
gear_last = 0
addx = 512
addy = 512
reconnected = False

def check_joy():
    global check_running, x_joy, x_joy_last, y_joy, y_joy_last, reconnected, joy
    while check_running == True:
        present = False
        cmd = "lsusb | grep -o ThrustMaster"
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]
        if output == 'ThrustMaster\n':
            present = True
        if present == False:
            print 'Joystick disconnected'
            reconnected = True
            y_joy = x_joy = x_joy_last = y_joy_last= 0
        if reconnected == True and present == True:
            pygame.joystick.quit()
            pygame.joystick.init()
            joy = pygame.joystick.Joystick(0)
            joy.init()
            reconnected = False

try:
    check_thread = threading.Thread(target=check_joy, args=())
    check_thread.start()

    while True:
        # time.sleep(0.01) #WHY?????? DOES THIS MAKE IT SMOOTH
        x_joy = x_joy_last 
        y_joy = y_joy_last
        gear = gear_last
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    x_joy = event.value*512 #-255 because the joystick was reverse mapped
                elif event.axis == 1:
                    y_joy = event.value*-512
                elif event.axis == 3:
                    gear = event.value

        x_joy_last = x_joy
        y_joy_last = y_joy
        gear_last = gear

        x_joy = int(x_joy)
        y_joy = int(y_joy)
        x_joy = x_joy + addx
        y_joy = y_joy + addy
        x_joy = max(min(1023, x_joy), 0)
        y_joy = max(min(1023, y_joy), 0)

        gear = int(((-gear+1)/2)*(numgears-1)) + 1

        print x_joy, y_joy, gear

        gear_bit0 = (0b00000001 & gear) << 5
        gear_bit1 = (0b00000010 & gear) << 4
        gear_bit2 = (0b00000100 & gear) << 3
        gear_bit3 = (0b00001000 & gear) << 2

        # print x_joy, y_joy, gear, gear_bit3>>5, gear_bit2>>5, gear_bit1>>5, gear_bit0>>5
        # make x
        tenbit2 = x_joy >> 5
        tenbit2 |= 0b11000000
        tenbit2 |= gear_bit1

        tenbit1 = x_joy & 0b00011111
        tenbit1 |= 0b10000000
        tenbit1 |= gear_bit0

        # make y
        tenbit4 = y_joy >> 5
        tenbit4 |= 0b00000000
        tenbit4 |= gear_bit3

        tenbit3 = y_joy & 0b00011111
        tenbit3 |= 0b01000000
        tenbit3 |= gear_bit2

        # send all
        ser.write(chr(tenbit1))
        ser.write(chr(tenbit2))
        ser.write(chr(tenbit3))
        ser.write(chr(tenbit4))

        # print '{0:x}'.format(tenbit1), '{0:x}'.format(tenbit2), '{0:x}'.format(tenbit3), '{0:x}'.format(tenbit4)

except KeyboardInterrupt:
    check_running = False
    check_thread.join()
    pass

print 'Exiting joystick...'
pygame.quit()
