import serial
import time
ser = serial.Serial('/dev/serial0', 115200)
while (1):
    ser.write('1')
    time.sleep(1)

