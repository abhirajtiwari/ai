import time
import rover_connections
from rover_connections import *
import numpy as np
#import rtimulsm
import math
from math import sin, cos, acos
from gps3.agps3threaded import AGPS3mechanism
import ultrasonic
import rover_core
import justimu


gps_thread = AGPS3mechanism()
gps_thread.stream_data()
gps_thread.run_thread()

num_gates = int(raw_input("Enter number of gates: "))

gates = []

allow_left = True
allow_right = True
allow_forward = True

speed = 128

try:
    #get gates
    for i in range(num_gates):
        gates.append(map(math.radians, map(float, raw_input('Enter gate {}: '.format(i)).split())))

    #append status
    for i in range(num_gates):
       gates[i].append(False) 

    #start auto
    for i, gate in enumerate(gates):
        if gates[num_gates-1][2] == True:
            break
        while gate[2] == False:
            curr = [math.radians(float(gps_thread.data_stream.lat)), math.radians(float(gps_thread.data_stream.lon))]

            #calculate distance
            dist = 1000 * 6371.01 * acos(sin(curr[0])*sin(gate[0]) + cos(curr[0])*cos(gate[0])*cos(curr[1] - gate[1]))

            #calculate coordinate heading
            x = cos(gate[0]) * sin(gate[1] - curr[1])
            y = cos(curr[0]) * sin(gate[0]) - sin(curr[0]) * cos(gate[0]) * cos(gate[1] - curr[1])
            head = math.atan2(x, y) * 180./np.pi
            if head < 0:
                head += 360

            #get rover heading
            #r_head = rtimulsm.getHeading() #rtimulsm
            r_head = justimu.getHead() ###LEANDER's CODE
            if r_head is None:
                r_head = last_head 
            last_head = r_head

            print r_head

            #check if the gate is complete 
            if dist < 2.5:
                print 'reached'
                gate[2] = True

            #get how to move 
            rotate_by = head - r_head

            if head >= r_head:
                if abs(rotate_by) >= 180:
                    turn_direction = False
                else:
                    turn_direction = True
            if r_head >= head:
                if abs(rotate_by) >= 180:
                    turn_direction = True
                else:
                    turn_direction = False

            #Ultrasonic conditions
            us_leftf = ultrasonic.getDistance(echolf, triggerlf)
            us_rightf = ultrasonic.getDistance(echorf, triggerrf)
            us_lefts = ultrasonic.getDistance(echols, triggerls)
            us_rights = ultrasonic.getDistance(echors, triggerrs)
            
            '''us_leftf = 300
            us_rightf = 300
            us_lefts = 300
            us_rights = 300'''

            if us_lefts < side_thresh:
                allow_left = False
            else:
                allow_left = True

            if us_rights < side_thresh:
                allow_right = False
            else:
                allow_right = True

            if us_leftf < front_thresh or us_rightf < front_thresh:
                allow_forward = False
            else:
                allow_forward = True

            # conditions where us is priority
            if us_leftf < front_thresh and us_rightf > front_thresh:#and rotate_by == 0:
                rover_core.right90(speed)
                continue
            elif us_leftf > front_thresh and us_rightf < front_thresh:# and rotate_by == 0:
                rover_core.left90(speed)
                continue
            elif  us_leftf < front_thresh and us_rightf < front_thresh:
                rover_core.uturn(speed)
                continue

            #Magneto conditions
            if rotate_by < 15 and rotate_by > -15:
                rotate_by = 0
            rotate_by = abs(rotate_by)
            print dist, r_head, rotate_by ####FOR DEBUG
            if rotate_by == 0 and allow_forward == True:
                rover_core.forward(speed)
            elif turn_direction == True and allow_right == True:
                rover_core.right0(speed)
            elif turn_direction == False and allow_left == True:
                rover_core.left0(speed)
            else:
                rover_core.forward(speed)

        print "Gate {} completed.\n".format(i)
        resp = raw_input("Proceed for next gate [n], switch to manual [m]: ")
        if resp != 'n' and resp != 'm':
            break

except KeyboardInterrupt:
    gpio.cleanup()

gpio.cleanup()
print 'Finished auto, Exiting...'
