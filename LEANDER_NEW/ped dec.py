import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.feature import hog
from skimage import data, exposure




cap = cv2.VideoCapture(0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5, 5))
kernel1= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3, 3))





while(1):

    # Take each frame
    _, frame = cap.read()

    
    frame=cv2.GaussianBlur(frame,(5,5),0)

    frame =cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel1)
    frame =cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel1)


    frame = cv2.erode(frame,kernel,iterations=2)
    frame = cv2.dilate(frame,kernel1, iterations=13)
    
    fd, hog_frame = hog(frame, orientations=8, pixels_per_cell=(16, 16),
                    cells_per_block=(1, 1), visualize=True, multichannel=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)

    ax1.axis('off')
    ax1.imshow(frame, cmap=plt.cm.gray)
    ax1.set_title('Input image')

    # Rescale histogram for better display
    hog_image_rescaled = exposure.rescale_intensity(hog_frame, in_range=(0, 10))

    ax2.axis('off')
    ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
    ax2.set_title('Histogram of Oriented Gradients')
    plt.show()	

    mask = cv2.cvtColor(hog_image_rescaled, cv2.COLOR_BGR2GRAY)    

# BOUNDING RECTANGLE .............................................................................................

    _, conts, hei = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    conts = np.array(conts)

    if len(conts) > 0:

        for i, contour in enumerate(conts):
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            aratio = (rect[1][0] / rect[1][1])
            if (aratio > 2) and (aratio < 3):
                cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

	    print("Aspect Ratio",aratio)

	    cv2.putText(frame,"PEDESTRIAN DETECTED",cv2.FONT_HERSHEY_SIMPLEX,2,255)






#DISPLAY................................................................................................................



    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    

#.....................................................................................................................
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()