#!/usr/bin/python

import argparse
import sys
import StringIO
import csv
import glob
from collections import OrderedDict
import re
import time
import datetime
import matplotlib.dates as mdate

class dataentry:
    """Data bean for VE direct data from 100/30 charge controller"""
    outputfields = OrderedDict([('V','Battery Volts'), ('I','Battery current'), ('VPV','Array Volts'), ('PPV','Array Watts'), ('CS','Charger State'), ('ERR','Error Code'), ('H19','Yield total(Wh)'), ('H20','Yield today(Wh)'), \
            ('H21','Max Power today(w)'), ('H22','Yield yesterday(Wh)'), ('H23','Max power yesterday(w)')])

    def __init__(self):
        self.data = dict()

    def addData(self, key, value):
        self.data[key] = value

    def outputData(self, seconds, outputfile):
        outputStr = None
        for key in self.outputfields:
            if key in self.data:
                if outputStr is None:
                    outputStr = str(seconds)
                outputStr += ',' + self.data[key]
        outputStr += '\n'
#        print outputStr
        outputfile.write(outputStr)

    def outputHeader(self, outputfile):
        outputStr = None
        
        for key in self.outputfields:
            if outputStr is None:
                outputStr = 'Seconds'
            outputStr += ',' + self.outputfields[key]
        outputStr += '\n'
#        print outputStr
        outputfile.write(outputStr)


parser = argparse.ArgumentParser(description='VE direct monthly data proc')
parser.add_argument('inputdir', help='Input dir to process',action='store')
parser.add_argument("outputfile", type=argparse.FileType('w'), help='Output file')

args = parser.parse_args()

print "Processing dir: ", args.inputdir
print "Output file: ", args.outputfile.name

entries = []

files = glob.glob(args.inputdir + "/*.csv")
files.sort()

with open(args.outputfile.name, 'wb') as outfile:
    outwrite = csv.writer(outfile, delimiter=',')
    outwrite.writerow(['Date','V start','V end','Yield (Wh)','Cumulative Yield(KWh)','Max power(w)'])
    for file in files:
        f = open(file,'r')
        filedate = re.search("([0-9]{4}\-[0-9]{2}\-[0-9]{2})", file)
        if ( filedate != None):
            print "Date: ", filedate.group()
            filedate = mdate.date2num(datetime.datetime.strptime(filedate.group(), "%Y-%m-%d"))
        else:
            continue
        data = csv.reader(f, delimiter=',')
        data.next()
        startVolts = 0
        yieldStart = 0

        while startVolts < 10000:
            row = data.next()
            startVolts = int(row[1])
        print "Starting voltage: ", startVolts
        
        endVolts = 0
        yieldEnd = 0
        maxPower = 0
        dayYield = 0
        for row in data:
            value = int(row[1])
            if value > 10000:
                endVolts = value
                yieldEnd = float(row[7])
                maxPower = int(row[11])
                dayYield = int(row[10]) * 10
        print "Ending voltage: ", endVolts
        print "Cumulative yield(KWh): ", yieldEnd/100
        print "Max power(w)", maxPower
        print "Yield total(Wh)", dayYield
        outwrite.writerow([filedate,startVolts,endVolts,dayYield,yieldEnd/100,maxPower])
        f.close()
