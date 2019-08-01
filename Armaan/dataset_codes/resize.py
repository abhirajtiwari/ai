import os 
import cv2

path="/home/armaan/Desktop/mrm/logi_dataset/lol/"
path1="/home/armaan/Desktop/mrm/logi_dataset/logi_noball/"
for file in os.listdir(path):
	img=cv2.imread(path+file)
	re=cv2.resize(img,(640,480))
	cv2.imwrite(path1+file,re)
	 
	 

