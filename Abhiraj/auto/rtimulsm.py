import RTIMU
import numpy as np
import math
import time

s = RTIMU.Settings('RTIMULib')
imu = RTIMU.RTIMU(s)

imu.IMUInit()

imu.setSlerpPower(0.02)
imu.setCompassEnable(True)

interval =  imu.IMUGetPollInterval()

def getHeading():
    if imu.IMURead():
        data = imu.getCompass()
        heading = math.atan2(data[1], data[0]) * 180./np.pi
        if heading < 0:
            heading += 360
        return heading

if __name__ == '__main__':
    while True:
        if imu.IMURead():
            data = imu.getCompass()
            heading = math.atan2(data[1], data[0]) * 180/np.pi
            if heading < 0:
                heading += 360
            print heading
            time.sleep(interval/1000.)
