import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)
ldir=9
lspeed=11
rdir=23
rspeed=24
gpio.setup(ldir,gpio.OUT)

gpio.setup(lspeed,gpio.OUT)

gpio.setup(rdir,gpio.OUT)

gpio.setup(rspeed,gpio.OUT)

ls=gpio.PWM(lspeed,100)
rs=gpio.PWM(rspeed,100)
ls.start(50)
rs.start(50)
def front():
	gpio.OUTPUT(ldir,1)
	gpio.OUTPUT(rdir,1)
	

while True:
	front()
