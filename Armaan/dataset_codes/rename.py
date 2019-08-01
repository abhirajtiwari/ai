import os 
import cv2
i=46
path="/home/armaan/Desktop/mrm/dataset_day2/ballnew/"
path1="/home/armaan/Desktop/mrm/dataset_day2/renamedballnew/"
for file in os.listdir(path):
	 src=path+file
	 dst=str(i)+".jpg"
	 dst=path1+dst
	 os.rename(src,dst)
	 i+=1
