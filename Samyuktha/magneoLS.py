import smbus2
import math
import numpy as np
bus= = smbus2.SMBus(1)
DEVICE_ADDRESS = 0x1e


bus.write_byte_data(DEVICE_ADDRESS,0x20,0b11101100)
bus.write_byte_data(DEVICE_ADDRESS,0x23,0b00001100)
bus.write_byte_data(DEVICE_ADDRESS,0x24,0b00000000)
def calc():
    xval_l = bus.read_byte_data(DEVICE_ADDRESS, 0x28)
    xval_m = bus.read_byte_data(DEVICE_ADDRESS, 0x29)
    yval_l = bus.read_byte_data(DEVICE_ADDRESS, 0x2A)
    yval_m = bus.read_byte_data(DEVICE_ADDRESS, 0x2B)
    zval_l = bus.read_byte_data(DEVICE_ADDRESS, 0x2C)
    zval_m = bus.read_byte_data(DEVICE_ADDRESS, 0x2D)
    xval = xval_m << 8 | xval_l
    yval = yval_m << 8 | yval_l
    zval = zval_m << 8 | zval_l
    x = twos_comp(xval, 16)
    y = twos_comp(yval, 16)
    z = twos_comp(zval, 16)
    print("X=",x)
    print("Y=",y)
    print("Z=",z)
    heading=math.atan2(y,x)*180./np.pi
    if heading<0:
        heading+=360
    print("heading=",heading)





def twos_comp(val, bits):

    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

def main():
    while True:
        calc()












