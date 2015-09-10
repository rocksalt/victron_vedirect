#!/usr/bin/python

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Gen graphs from VE direct overview CSV files.')
parser.add_argument('inputfile', type=argparse.FileType('r'), help='Input file to process (.csv)')
args = parser.parse_args()

data = np.genfromtxt(args.inputfile.name, dtype=[('a','float64'),('b','int32'),('c','int32'),('d','int32'),('e','float64'),('f','int32')], delimiter=',', skip_header=1,
        skip_footer=0 )
fig = plt.figure(figsize=(20,10))
ax1 = fig.add_subplot(1,1,1)
ax1.set_title(args.inputfile.name)
ax1.set_xlabel('Date')
ax1.set_ylabel('KWh')
#xmax = max([max(data['a'])])
#print "Max: ", xmax
#dates = mpl.dates.datestr2num(data['a'])
dates = data['a']
p1, = ax1.plot_date(dates, data['e'], color='k', label='Cumulative yield(KWh)', xdate=True, linestyle='-', marker='x',linewidth=2.0)
ax1.xaxis.grid(b=True, color='black', linestyle=':')
ax1.yaxis.grid(b=True, color='black', linestyle='--')
#p2, = ax1.plot(dates,data['c'], color='b', label='V - end', linestyle='-', marker="^")


ax2 = ax1.twinx()
p3, = ax2.plot(dates,data['d'], color='g', label='Yield (Wh)', linestyle='-',marker='+')
#p4, = ax2.plot(dates,data['f'], color='k', label='Max power (W)', linestyle='-.', marker='x')
#ax2.grid(b=True, which='both', color='black', linestyle='--')
ax2.set_ylabel('Wh')



leg = ax1.legend()
leg2 = ax1.legend(handles=[p1,p3], loc=1, prop={'size':12})
#plt.xlim(0,xmax)
#plt.savefig(args.inputfile.name + ".png", dpi = 300)
plt.show()

