import cv2
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt

#%config InlineBackend.figure_format = 'svg'

options = {
		'model': 'cfg/yolo.cfg',
		'load': 'bin/yolov2.weights',
		'threshold': 0.3,
}

tfnet = TFNet(options)

img = cv2.imread('tennis.jpg',cv2.IMREAD_COLOR)
result = tfnet.return_predict(img)

print(result)

topL = (result[0]['topleft']['x'],result[0]['topleft']['y'])
bottomR = (result[0]['bottomright']['x'],result[0]['bottomright']['y'])

label = result[0]['label']

img = cv2.rectangle(img, topL, bottomR, (0,255,255))
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.show()
