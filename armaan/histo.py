import cv2
import numpy as np
from matplotlib import pyplot as plt

img=cv2.imread('103.jpg')
img_yuv=cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
"""clahe=cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
img_yuv[:,:,0]=clahe.apply(img_yuv[:,:,0])
img_output=cv2.cvtColor(img_yuv,cv2.COLOR_YUV2BGR)
#img_output=cv2.cvtColor(img_output,cv2.COLOR_BGR2HSV)
img=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
"""

"""
hmin=20
smin=117
vmin=38
hmax=100
smax=255
vmax=255
lball=np.array([hmin,smin,vmin]
hball=np.array([hmax,smax,vmax])
mask1=cv2.inRange(img_output,lball,hball)
mask=cv2.inRange(img,lball,hball)
"""

cv2.imshow('res',img)
hist=cv2.calcHist([img_yuv],[0],None,[256],[0,256])
plt.plot(hist,color='r')
plt.xlim([0,256])
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
