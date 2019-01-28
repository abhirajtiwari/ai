import cv2,glob
images=glob.glob("*.jpg")
i=0
for image in images:
    i+=1
    img=cv2.imread(image,1)
    re=cv2.resize(img,(640,480))  #width,height
    cv2.imshow("checking",re)
    cv2.waitKey(500)
    cv2.destroyAllWindows()
    #name = str(i) + '.jpg'

    cv2.imwrite(r'C:\Users\Samyuktha Raj\Desktop\random1\image.jpg', re)