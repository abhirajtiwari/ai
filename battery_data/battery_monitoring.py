import matplotlib.pyplot as plt
import numpy as np
import time
from scipy.ndimage.interpolation import shift
from matplotlib.gridspec import GridSpec
import serial

refresh_rate = 1

ser = serial.Serial('/dev/ttyUSB0', 38400)

x = np.linspace(0, 15, 100)
zeros = np.zeros_like(x)

curr_value = 0

plt.ion()

fig = plt.figure()

#Current graph init
curr_gridspec = GridSpec(1, 7).new_subplotspec((0,0), colspan=5)
curr_graph = fig.add_subplot(curr_gridspec)
curr_graph.axes.get_xaxis().set_visible(False)
curr_graph.grid()
curr_graph.set_title('Current')
curr_data, = curr_graph.plot(x, curr_value*np.ones_like(x), 'b-') 

#Battery state graph init
soc = 0
batt_gridspec = GridSpec(1, 7).new_subplotspec((0,6), colspan=1)
battery_graph = fig.add_subplot(batt_gridspec)
battery_graph.axes.get_xaxis().set_visible(False)
battery_graph.set_title('Battery')
battery_graph.set_ylim((0,110))
battery_bar, = battery_graph.bar(1, soc, align='center')

while True:

    #current graph stuff
    ##Get current value here and do something with it
    zeros[-1] = curr_value+np.random.random()
    if zeros[-1] > 5:
        curr_data.set_color('r')
    else:
        curr_data.set_color('b')
    curr_data.set_ydata(shift(curr_data.get_ydata(), -1, cval=0)+zeros)
    curr_graph.relim()
    curr_graph.autoscale_view()

    #battery graph stuff
    ##Get soc here and plot it
    battery_bar.set_height(50)
    battery_graph.set_title('Battery: %d' % soc)

    fig.canvas.draw()
    fig.canvas.flush_events()
