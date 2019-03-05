import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

echo_left = 17
trigger_left = 27
echo_right = 15
trigger_right = 14
echo_side_l = 19
trigger_side_l = 26
echo_side_r = 21
trigger_side_l = 20


GPIO.setup(trigger_left, GPIO.OUT)
GPIO.setup(echo_left, GPIO.IN)

GPIO.setup(trigger_right, GPIO.OUT)
GPIO.setup(echo_right, GPIO.IN)

GPIO.setup(trigger_side_l, GPIO.OUT)
GPIO.setup(echo_side_l, GPIO.IN)

GPIO.setup(trigger_side_r, GPIO.OUT)
GPIO.setup(echo_side_r, GPIO.IN)

def Ultrasonic(pin):
	GPIO.output(pin,False)
	time.sleep(0.1)

	GPIO.output(pin,True)
	time.sleep(0.00001)
	GPIO.output(pin,False)
	while GPIO.input(pin) != GPIO.HIGH:
		pass
	pulse_begins = time.time()
	while GPIO.input(pin) == GPIO.HIGH:
		pulse_stops = time.time()
		pulse_duration = pulse_stops - pulse_begins
		if pulse_duration > limit:
			distance = pulse_duration * 34000/2
			return distance,'alert'
		return distance,'not alert'

while True:
	dist_lf,alert_lf = Ultrasonic(echo_left)
	dist_rf,alert_rf = Ultrasonic(echo_right)
	dist_sl, alert_l = Ultrasonic(echo_side_l)
	dist_sr, alert_r = Ultrasonic(echo_side_r)
	#print(alert_r,alert_l,alert_rf,alert_lf)
	if alert_rf == 'alert' and alert_lf == 'not alert':
		print('turn left') 
	elif alert_lf == 'alert' and alert_rf == 'not alert':
		print('turn right')
 	elif dist_lf > dist_rf:
 		print('turn right')
 	else:
 		print('turn left')

 	if (alert_rf == 'not alert' and alert_lf == 'not alert'):
 		print('straight')
 		if alert_l == 'alert':
 			print('cant turn left even if imu is saying')
 			print('go straight until alert_l == not alert')

 		elif alert_r == 'alert':
 			print('cant turn right even if imu is saying')
 			print('go straight until alert_r == not alert')
