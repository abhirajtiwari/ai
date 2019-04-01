import subprocess
import signal
import os

mode = 'm'
cam_pid = 1e8
joy_pid = 1e8

def auto():
    print 'Starting auto...'
    subprocess.Popen(['python', 'tennis_fin.py']).wait() #auto

def manual():
    global cam_pid
    global joy_pid
    try:
        cam_pid = subprocess.Popen(['konsole', '-e', 'python', '/home/abhiraj/Mars Rover Manipal/ai/Abhiraj/client_encoded.py']).pid 
        print 'Started camera'
    except:
        print 'Unable to start camera'

    try:
        joy_pid = subprocess.Popen(['konsole', '-e', 'python', '/home/abhiraj/Mars Rover Manipal/ai/Abhiraj/joystick_w_atmega.py']).pid
    except:
        print 'Unable to start joystick'
    print 'Started joystick'

    char = raw_input("Press 'e' to exit | Press 'a' for auto...\n")
    return char

while True:
    char = manual()
    if char == 'e':
        os.kill(int(cam_pid), signal.SIGINT)
        os.kill(int(joy_pid), signal.SIGINT)
        break
    elif char == 'a':
        os.kill(int(joy_pid), signal.SIGINT)
        os.kill(int(cam_pid), signal.SIGINT)
        auto()
