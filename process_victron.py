#!/usr/bin/python

import argparse
import sys
from collections import OrderedDict

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


parser = argparse.ArgumentParser(description='VE direct tty text dump processor.')
parser.add_argument('inputfile', type=argparse.FileType('r'), help='Input file to process')
parser.add_argument("outputfile", type=argparse.FileType('w'), help='Output file')

args = parser.parse_args()

print "Processing file: ", args.inputfile.name
print "Output file: ", args.outputfile.name

entries = []

outputfile = open(args.outputfile.name, 'w')

ent = dataentry()
secondCounter = 1
ent.outputHeader(outputfile)
for line in open(args.inputfile.name):
 if line.startswith("Checksum"):
  entries.append(ent)
  ent.outputData(secondCounter, outputfile)
  secondCounter += 1
  ent = dataentry()
 else:
     keyval = line.split("\t", 1)
#     print "Input: ", line
#     print "Keyval: ", keyval
     if len(keyval) == 2:
      ent.addData(keyval[0].strip(), keyval[1].strip())

outputfile.close()

