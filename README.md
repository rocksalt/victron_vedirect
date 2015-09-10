In my previous house I made an off grid solar setup consisting of 2x195w panels, A victron 100/30 controller and 200Ah of battery storage.  I ran it between Feb and August 2015. 

I used these scripts to process the VE.Direct TTY output from my Victron 100/30 Solar charge controller daily, using a Raspberry PI and an el-cheapo TTY-USB converter.  Maybe some one else will find them useful.

The various scripts are used for the following:

1) Data processing.

process_victron.py is the tty output processing script.  This script is used to convert the captured raw tty output from the controller (e.g. using cat /dev/ttyUSB0 > output.file) 
into a csv format for graphing.

2) Graphing.  

There are a bunch of dirty scripts to generate graphs from the .csv files using matplotlib.  Use/modify as required, matplotlib can do a lot and I'm probably just scratching the surface.
gen_graph.py is the main one and was used to create a graph of the day's solar yield.  The other scripts can be used to output graphs of monthly summary outputs (generated using the other scripts).

I've added a doc outlining the VE.Direct protocol description as downloaded from the Victron website.

You can find some samples of the raw tty output, the processed csv file and a graph generated using gen_graph.py in the samples directory.
