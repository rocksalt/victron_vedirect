#!/usr/bin/python

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Gen graphs from VE direct CSV dumps.')
parser.add_argument('inputfile', type=argparse.FileType('r'), help='Input file to process (.csv)')
args = parser.parse_args()

data = np.genfromtxt(args.inputfile.name, delimiter=',', skip_header=1,
        skip_footer=0, names=['a', 'b', 'c','d','e'])
fig = plt.figure(figsize=(20,10))
ax1 = fig.add_subplot(1,1,1)
ax1.set_title(args.inputfile.name)
ax1.set_xlabel('Data snapshot')
ax1.set_ylabel('mV')
xmax = max([max(data['a'])])
print "Max: ", xmax
p1, = ax1.plot(data['a'], data['d'], color='r', label='PV Voltage')
ax1.xaxis.grid(b=True, color='black', linestyle=':')
p2, = ax1.plot(data['a'],data['b'], color='b', label='Batt voltage')


ax2 = ax1.twinx()
p3, = ax2.plot(data['a'],data['e'], color='g', label='PV Watts' )
ax2.grid(b=True, which='both', color='black', linestyle='--')
ax2.set_ylabel('W')



leg = ax1.legend()
leg2 = ax1.legend(handles=[p1,p2,p3], loc=1, prop={'size':12})
plt.xlim(0,xmax)
plt.savefig(args.inputfile.name + ".png", dpi = 400)
plt.show()

