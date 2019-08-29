import time
import numpy as np
import rtimulsm
import math
from math import sin, cos, acos
from gps3.agps3threaded import AGPS3mechanism

gps_thread = AGPS3mechanism()
gps_thread.stream_data()
gps_thread.run_thread()

num_gates = int(raw_input("Enter number of gates: "))

gates = []


#Get gates
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
        r_head = rtimulsm.getHeading() #rtimulsm
        if r_head is None:
            r_head = last_head 
        last_head = r_head

        #check if the gate is complete 
        if dist < 2.5:
            print 'reached'
            gate[2] = True
        # print dist, head, r_head

        #get how to move 
        rotate_by = head - r_head
        turn_direction = True if abs(rotate_by) >= 180 else False  #true means clockwise
        if rotate_by < 15 and rotate_by > -15:
            rotate_by = 0
        rotate_by = abs(rotate_by)
        print dist, rotate_by, "Clockwise" if turn_direction==True else "Anti-Clockwise"
        #Here appropriate calls should be made to ATmega

    print "Gate {} complet.\n".format(i)
    resp = raw_input("Proceed for next gate [n], switch to manual [m]: ")
    if resp != 'n' and resp != 'm':
        break

print 'Finished auto, Exiting...'
