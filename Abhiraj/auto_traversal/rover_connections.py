import RPi.GPIO as gpio

###MOTORS###
motorl = 9 
motorlp = 11
motorr = 23
motorrp = 24

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
side_thresh = 20
front_thresh = 30

triggerrf = 14
echorf = 15
triggerlf = 27
echolf = 17
triggerrs = 20
echors = 21
triggerls = 26
echols = 19

gpio.setup(echorf, gpio.IN)
gpio.setup(echolf, gpio.IN)
gpio.setup(echors, gpio.IN)
gpio.setup(echols, gpio.IN)

gpio.setup(triggerrf, gpio.OUT)
gpio.setup(triggerlf, gpio.OUT)
gpio.setup(triggerrs, gpio.OUT)
gpio.setup(triggerls, gpio.OUT)

