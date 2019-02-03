import smbus
import time

sb = sumbus.SMBus(1)   #1 start byte

sb.write_byte_data(0x1E, 0x20, 0b11111100)      #0x1E is the address of magnetometer
sb.write_byte_data(0x1E, 0x21, 0b00000000)      #0x20 is the register
sb.write_byte_data(0x1E, 0x22, 0b00000000)      #0b11111100 is the data to write on those registers
sb.write_byte_data(0x1E, 0x23, 0b00001100)

x_mag = sb.read_byte_data(0x1E, 0x28)
y_mag = sb.read_byte_data(0x1E, 0x2A)
z_mag = sb.read_byte_data(0x1E, 0x2C)
print('x_value',x_mag)
print('y_value',x_mag)
print('z_value',x_mag)
