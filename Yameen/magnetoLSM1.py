import smbus
import time
import math as m

sb = smbus.SMBus(1)   #1 start byte

sb.write_byte_data(0x1E, 0x20, 0b11111100)      #0x1E is the address of magnetometer
sb.write_byte_data(0x1E, 0x21, 0b00000000)      #0x20 is the register
sb.write_byte_data(0x1E, 0x22, 0b00000000)      #0b11111100 is the data to write on those registers
sb.write_byte_data(0x1E, 0x23, 0b00001100)

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val

'''
def ans():
    if (x_mag>0):
        print('14 x>0')
        pos1 = 2*m.atan2(y_mag,x_mag)
        if pos1>0:
            return pos1
        else:
            return pos1 + m.pi*2
    #elif (x_mag<0 and y_mag>=0):
    elif (x_mag<0):
        print('23 x<0')
        pos2 = 2*m.pi - 2*m.atan2(y_mag,-x_mag)
        if pos2>0:
            return pos2
        else:
            return pos2 + m.pi*2
'''

def ans():
    if (x_mag>0 and y_mag>0):
        print('1 x>0 y>0')
        pos1 = m.atan(y_mag/x_mag)
        return pos1                 #0 to 90

    elif (x_mag<0 and y_mag>0):
        print('2 x<0 y>0')
        pos2 =  m.atan(y_mag/x_mag)
        return pos2 + m.pi          #90 to 180

    elif (x_mag<0 and y_mag<0):
        print('3 x<0 y<0')
        pos2 =  m.atan(y_mag/x_mag)
        return pos2 + m.pi          #180 to 270

    elif (x_mag>0 and y_mag<0):
        print('4 x>0 y<0')
        pos2 =  m.atan(y_mag/x_mag)
        return pos2 + 2*m.pi        #270 to 360

while True:

    x_l = sb.read_byte_data(0x1E, 0x28)
    x_h = sb.read_byte_data(0x1E, 0x29)
    x_mag = twos_comp(x_h << 8 | x_l, 16)
    y_l = sb.read_byte_data(0x1E, 0x2A)
    y_h = sb.read_byte_data(0x1E, 0x2B)
    y_mag = twos_comp(y_h << 8 | y_l, 16)
    z_l = sb.read_byte_data(0x1E, 0x2C)
    z_h = sb.read_byte_data(0x1E, 0x2D)
    z_mag = twos_comp(z_h << 8 | z_l, 16)
    print('x_value',x_mag)
    print('y_value',y_mag)
    #print('z_value',z_mag)

    heading = ans()*180/m.pi
    print(heading)


'''
def translate(heading, 0, 359, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
'''


#valueScaled = float(value - leftMin) / float(leftSpan)
