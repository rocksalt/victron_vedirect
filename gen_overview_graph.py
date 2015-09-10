#!/usr/bin/python

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse

def autolabel(rects,color,heightmult):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., height*heightmult, '%d'%int(height),
        ha='center', va='bottom',color=color)

parser = argparse.ArgumentParser(description='Gen graphs from VE direct overview CSV files.')
parser.add_argument('inputfile', type=argparse.FileType('r'), help='Input file to process (.csv)')
args = parser.parse_args()

data = np.genfromtxt(args.inputfile.name, dtype=[('float64'),('int32'),('int32'),('int32'),('float64'),('int32')], delimiter=",", skip_header=1,
        names="a,b,c,d,e,f", skip_footer=0, autostrip=True )

fig = plt.figure(figsize=(20,10))
ax1 = fig.add_subplot(1,1,1)
ax1.set_title(args.inputfile.name)
ax1.set_xlabel('Date')
ax1.set_ylabel('mV')

dates = mpl.dates.num2date(data['a'])
p1, = ax1.plot_date(dates, data['b'], color='r', label='V - start', xdate=True, linestyle='-', marker='.')
ax1.xaxis.grid(b=True, color='black', linestyle=':')
ax1.yaxis.grid(b=True, color='black', linestyle='--')
p2, = ax1.plot(dates,data['c'], color='b', label='V - end', linestyle='-', marker="^")
ax1.fill_between(dates, data['b'], data['c'])
ax1.fill_between(dates, 11400, data['b'], color='yellow')


ax2 = ax1.twinx()
p3 = ax2.bar(dates,data['d'], color='g', label='Yield (Wh)', width=0.2)
p4 = ax2.bar(dates,data['f'], color='k',label='Max power (W)',align='center',width=0.2)
ax2.grid(b=True, which='both',  color='black', linestyle='--')
ax2.set_ylabel('Wh (W)')
autolabel(p3,'red',1)
autolabel(p4,'magenta',0.8)


leg = ax1.legend()
leg2 = ax1.legend(handles=[p1,p2,p3,p4], loc=1, prop={'size':12})
plt.show()

