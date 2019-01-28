import os
from os import path


# Function to rename multiple files

i = 1

for filename in os.listdir(r"C:\Users\Samyuktha Raj\Desktop\with ball"):
    if path.exists(r"C:\Users\Samyuktha Raj\Desktop\with ball"):
        src=path.realpath(r"C:\Users\Samyuktha Raj\Desktop\with ball")
        dst = r"C:\Users\Samyuktha Raj\Desktop\with ball"+'\\'+str(i) + ".jpg"
        src = r"C:\Users\Samyuktha Raj\Desktop\with ball"+'\\'+filename
        #dst += dst

        # rename() function will
        # rename all the files
        os.rename(src, dst)
        i += 1



