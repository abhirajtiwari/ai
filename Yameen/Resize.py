from PIL import Image
import os, sys

path = "/home/nemaye/Pictures/dataset/withBall/"
dirs = os.listdir( path )
i = [1,200]

for item in dirs:
    if os.path.isfile(path+item):
        im = Image.open(path+item)
        _, e = os.path.splitext(path+item)          #see below comment
# first return value stores the directory the stored file and the second return value stores the extension of the file
        imResize = im.resize((645,480), Image.ANTIALIAS)
        for list in i:
            imResize.save('/home/nemaye/Pictures/resized/',+str(i),'.jpg' 'JPEG', quality=90)



#if aspect ratio of the original image is not 4:3 then crop it and then resize
