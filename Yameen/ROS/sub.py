import rospy
from sensor_msgs.msg import LaserScan,Imu,NavSatFix
from geometry_msgs.msg import Twist
import time
from tf.transformations import euler_from_quaternion
import math

obj = Twist()
arr_l = []
arr_r = []
arr_m = []
pub = rospy.Publisher('ddrobot/velocity', Twist, queue_size=10)
rospy.init_node('listener', anonymous=True)

lat = 49.90080613209061
lon2 = 81.900778560940432

distance = 0.00
heading = 0
ml = 0
mr = 0
min_val = 0
degree = 0

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min



def callback(msg):
	#time.sleep(0.2)
	#print('da',msg.ranges)
	global ml,mr,min_val
	
	front_left = front_right = right_lidar = left_lidar = 'not alert'
	#print(front_left,front_right,right_lidar,left_lidar)
	arr_ml = [msg.ranges[0],msg.ranges[1],msg.ranges[2]]
	arr_mr = [msg.ranges[7],msg.ranges[8],msg.ranges[9]]
	arr_m = [msg.ranges[3],msg.ranges[4],msg.ranges[5],msg.ranges[6]]
	ml = min(arr_ml)
	mr = min(arr_mr)
	min_val = min(arr_m)
	turn = heading - degree		
	#print('cds',min_val)
	#print('tuen is',turn)	
	#print('h',heading,degree,turn,distance,'cs',msg.ranges[3],msg.ranges[6])
	if ml<3.5:
		right_lidar = 'alert'
		print('alert1')
	if mr<3.5:
		left_lidar = 'alert'
		print('alert2')
	if msg.ranges[3] < 3.5 or msg.ranges[4] < 3.5:
		front_right = 'alert'
		print('alert3')
	if msg.ranges[5] < 3.5 or msg.ranges[6] < 3.5:
		front_left = 'alert'
		print('alert4')
	
	
	if ((front_left == 'alert' and front_right == 'not alert') or (front_left == 'alert' and front_right == 'alert')):
		obj.linear.x = 0
		obj.angular.z = 1
		pub.publish(obj)
		print('this loop')

	elif front_right == 'alert' and front_left == 'not alert':
		obj.linear.x = 0
		obj.angular.z = -1
		pub.publish(obj)

	print(front_left,front_right,right_lidar,left_lidar)

	if 	front_left == 'not alert' and front_right == 'not alert':
		if (right_lidar == 'alert' and left_lidar == 'not alert'):
			if turn<-190:
				obj.linear.x = 0
				obj.angular.z = -1
				pub.publish(obj)
				print('11')
			elif turn>10 and turn<170:
				obj.linear.x = 0
				obj.angular.z = -1
				pub.publish(obj)
				print('22')
			else:
				obj.linear.x = 0.5
				obj.angular.z = 0
				pub.publish(obj)
				print('1')
		elif (right_lidar == 'not alert' and left_lidar == 'alert'):
			if turn<-15 and turn>-165:
				obj.linear.x = 0
				obj.angular.z = 1
				pub.publish(obj)
			elif turn>=195:
				obj.linear.x = 0
				obj.angular.z = 1
				pub.publish(obj)
			else:
				obj.linear.x = 0.5
				obj.angular.z = 0
				pub.publish(obj)
				print('2')

		elif right_lidar == 'not alert' and left_lidar == 'not alert':
			if turn<=-195:
				obj.linear.x = 0
				obj.angular.z = -1
				pub.publish(obj)
				print('33')
			elif turn>15 and turn<165:
				obj.linear.x = 0
				obj.angular.z = -1
				pub.publish(obj)
				print('44')
			elif turn<-15 and turn>-165:
				obj.linear.x = 0
				obj.angular.z = 1
				pub.publish(obj)
			elif turn>0 and turn>=195:
				obj.linear.x = 0
				obj.angular.z = 1
				pub.publish(obj)
			else:
				obj.linear.x = 0.5
				obj.angular.z = 0
				pub.publish(obj)
				print('3')
	
		else:
			obj.linear.x = 0.5
			obj.angular.z = 0
			pub.publish(obj)
	'''
	else:
		obj.linear.x = 0.5
		obj.angular.z = 0
		pub.publish(obj)
		print('4') 
	'''

	'''

	if min_val<2:
		obj.linear.x = 0
		obj.angular.z = 0
		pub.publish(obj)
	else:
		if turn < 20 or turn > 340:
			obj.linear.x = 0
			obj.angular.z = 0
			pub.publish(obj)
			#print('rhis shoud woork')
		else:
			obj.linear.x = 0
			obj.angular.z = 0
			pub.publish(obj)
			#print('is tehs worjinf')	
'''
	
def callback_imu(msg):
	#print('xsax',msg.orientation.x,msg.orientation.y,msg.orientation.z)
	#rospy.sleep(0.01)
	global heading
	orientation_list=[msg.orientation.x,msg.orientation.y,msg.orientation.z,msg.orientation.w]
	(roll,pitch,yaw)=euler_from_quaternion(orientation_list)
	heading=map(yaw,0,-3,0,180)
	if heading<0:
		heading = heading + 360
	#print('head',heading)
	

def callback_gps(msg):
	global distance,degree
	lat1 = msg.latitude
	lon1 = msg.longitude
	#print('err',lat1,lon1,lat,lon2)
	dLat = (lat - lat1) * math.pi / 180.0
	dLon = (lon2 - lon1) * math.pi / 180.0
	lat1 = lat1 * math.pi / 180.0
	lat2 = lat * math.pi / 180.0

	y = math.cos(lat2) * math.sin(dLon)
	x = (math.cos(lat1) * math.sin(lat2)) - (math.sin(lat1) * math.cos(lat2) * math.cos(dLon))
	degree = math.atan2(y, x) * 180 / math.pi
	if degree < 0:
		degree += 360
	#print('deg',degree)
	a = (pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(lat1) * math.cos(lat))
	rad = 6378.1*1000
	c = 2 * math.asin(math.sqrt(a))
	distance = rad * c
	#print('dist',distance) 

def talker():
	pass
    #rate.sleep()

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
	rospy.Subscriber('/imu', Imu, callback_imu)
	print('test')
	print('tesd')
		
	rospy.Subscriber('/gps',NavSatFix,callback_gps)
	rospy.Subscriber('sensor/lidar', LaserScan, callback)
	print('dfsvdfv')
	while not rospy.is_shutdown():
		#print('dasd')
		
				
		
		rospy.sleep(10)
		#print('dasdadg')
    # spin() simply keeps python from exiting until this node is stopped
    
		#rospy.sleep(0.1)
    	#print('dshb')

if __name__ == '__main__':
    listener()
    #print('da')
    #while True:
    #	talker()