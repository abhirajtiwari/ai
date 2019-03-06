import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

echo_left = 17
trigger_left = 27
echo_right = 15
trigger_right = 14
echo_side_l = 19
trigger_side_l = 26
echo_side_r = 21
trigger_side_r = 20


GPIO.setup(trigger_left, GPIO.OUT)
GPIO.setup(echo_left, GPIO.IN)

GPIO.setup(trigger_right, GPIO.OUT)
GPIO.setup(echo_right, GPIO.IN)

GPIO.setup(trigger_side_l, GPIO.OUT)
GPIO.setup(echo_side_l, GPIO.IN)

GPIO.setup(trigger_side_r, GPIO.OUT)
GPIO.setup(echo_side_r, GPIO.IN)

def Ultrasonic(pin,pin2):
	GPIO.output(pin2,False)
	time.sleep(0.1)

	GPIO.output(pin2,True)
	time.sleep(0.00001)
	GPIO.output(pin2,False)

	while GPIO.input(pin)==0:
		pass
	pulse_begins = time.time()
	
	while GPIO.input(pin)==1:
		pulse_stops = time.time()
		if (pulse_stops-pulse_begins>0.004):
			pulse_duration = pulse_stops-pulse_begins
			distance = pulse_duration*34000/2
			return distance,'not alert'
			break
	
	pulse_duration = pulse_stops-pulse_begins
	distance = pulse_duration*34000/2
	return distance,'alert'

while True:
	dist_lf,alert_lf = Ultrasonic(echo_left,trigger_left)
	dist_rf,alert_rf = Ultrasonic(echo_right,trigger_right)
	dist_sl, alert_l = Ultrasonic(echo_side_l,trigger_side_l)
	dist_sr, alert_r = Ultrasonic(echo_side_r,trigger_side_r)
	#print(alert_r,alert_l,alert_rf,alert_lf)
	if alert_rf == 'alert' or alert_lf == 'alert':
		if dist_lf < dist_rf:
 			print('right')
 		else:
 			print('left')
 	

 	elif (alert_rf == 'not alert' and alert_lf == 'not alert'):
 		print('straight')
 		if alert_l == 'alert':
 			#rint('cant turn left even if imu is saying')
 			print('go straight')# until alert_l == not alert

 		elif alert_r == 'alert':
 			#rint('cant turn right even if imu is saying')
 			print('go straight')# until alert_r == not alert

 	
