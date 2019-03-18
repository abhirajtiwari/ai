import RPi.GPIO as gpio

###MOTORS###
motorl = 5
motorlp = 13
motorr = 23
motorrp = 18

gpio.setmode(gpio.BCM)

gpio.setup(motorl, gpio.OUT)
gpio.setup(motorlp, gpio.OUT)
gpio.setup(motorr, gpio.OUT)
gpio.setup(motorrp, gpio.OUT)

lpwm = gpio.PWM(motorlp, 50)
rpwm = gpio.PWM(motorrp, 50)

lpwm.start(0)
rpwm.start(0)

###ULTRASONICS###
side_thresh = 30
front_thresh = 30

triggerrf = 9
echorf = 11
triggerlf = 19
echolf = 26
triggerrs = 8
echors = 25
triggerls = 20
echols = 16

gpio.setup(echorf, gpio.IN)
gpio.setup(echolf, gpio.IN)
gpio.setup(echors, gpio.IN)
gpio.setup(echols, gpio.IN)

gpio.setup(triggerrf, gpio.OUT)
gpio.setup(triggerlf, gpio.OUT)
gpio.setup(triggerrs, gpio.OUT)
gpio.setup(triggerls, gpio.OUT)

