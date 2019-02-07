
#offset
import smbus
import time
import math
import numpy as np
add=0x1e
i2c=smbus.SMBus(1)
i2c.write_byte_data(add,0x20,0b01011100)#high performance
i2c.write_byte_data(add,0x21,0b00000000)#4 gauss range
i2c.write_byte_data(add,0x22,0b00000000)
i2c.write_byte_data(add,0x23,0b00001000)
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val        

def map(x,in_min,in_max,out_min,out_max):
	return ((x-in_min)*(out_max-out_min)/(in_max-in_min))+out_min



while (1):
	msbx=i2c.read_byte_data(add,0x29)
	lsbx=i2c.read_byte_data(add,0x28)
	x=(msbx<<8|lsbx)
	x=twos_comp(x,16)*0.00014
	msby=i2c.read_byte_data(add,0x2b)
	lsby=i2c.read_byte_data(add,0x2a)
	y=(msby<<8|lsby)
	y=twos_comp(y,16)*0.00014	
	msbz=i2c.read_byte_data(add,0x2d)
	lsby=i2c.read_byte_data(add,0x2c)
	z=(msbz<<8|lsbz)
	x=x-0.06
	y=y-0.35
	h=math.atan2(y,x)*180/np.pi
	if h<0:
		h+=360
	
	print h
	
