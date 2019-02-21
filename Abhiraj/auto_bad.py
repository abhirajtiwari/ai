import time
import numpy as np
# import rtimulsm
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

for i, gate in enumerate(gates):
    if gates[num_gates-1][2] == True:
        break
    while gate[2] == False:
        curr = [math.radians(float(gps_thread.data_stream.lat)), math.radians(float(gps_thread.data_stream.lon))]

        #calculate distance
        dist = 1000 * 6371.01 * acos(sin(curr[0])*sin(gate[0]) + cos(curr[0])*cos(gate[0])*cos(curr[1] - gate[1]))

        #calculate heading
        x = cos(gate[0]) * sin(gate[1] - curr[1])
        y = cos(curr[0]) * sin(gate[0]) - sin(curr[0]) * cos(gate[0]) * cos(gate[1] - curr[1])
        head = math.atan2(x, y) * 180./np.pi
        if head < 0:
            head += 360

        if dist < 2:
            print 'reached'
            gate[2] = True
        print dist, head

print 'Finished auto, Exiting...'
