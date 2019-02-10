
filename = "fifo.tmp"
import subprocess
while(1):
# Block until writer finishes...
    #time.sleep(10)
    with open(filename, 'r') as f:
        data = f.read()
    #array = [int(x) for x in data.split()]
# Split data into an array
    print data
"""subprocess.call(["gcc", "fifo.c"])
tmp=subprocess.call("./a.out")
"""
