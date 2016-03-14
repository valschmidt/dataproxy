#!/usr/bin/env python
#
# Val Schmidt
# Center for Coastal and Ocean Mapping
# Univeristy of New Hampshire
# Copyright 2016

import _mypath
import dataproxy
import time
import sys
import serial as ser


# Set up argument parsing.                                                                                         
import argparse
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument("-f","--forwarder",
                    action = "store",
                    default = "localhost",
                    help = "IP address or DNS name of the forwarder")
parser.add_argument("-i","--topicID",
                    action = "store",
                    default = "TEST_123",
                    help = "Text string for ID of this published topic.")
group.add_argument("-t","--test_file",
                    action = "store",
                    default = "",
                    help = "File of test messages (1 per line)")
group.add_argument("-p","--port",
                    action = "store",
                    default = "/dev/ttyS0:9600",
                    help = "Serial port:baudrate from which to read data (e.g. /dev/ttyS0:9600)")

parser.add_argument("-l","--log_locally",
                    action = "store_true",
                    default = False,
                    help = "Log images locally [NOT IMPLEMENTED]")
parser.add_argument("-v","--verbosity",
                    action = "count",
                    help = "Verbose output to terminal")
parser.add_argument("-T","--transport",
                    action = "store",
                    choices = ["s","p","b","zb","n"],
                    default = "s",
                    help = "Set transport method: string, compressed pickle, binary, compressed binary, numpy")

class publisher(dataproxy.publisher):

    def get_test_data(self):
        time.sleep(1)
        line = TESTFILE.readline()
        # Restart at the beginning if we get to the end.
        if line == "":
            TESTFILE.seek(0)
            line = TESTFILE.readline()
        return line

    def get_serial_data(self):
        line = serialport.readline()
        return line

if __name__ == "__main__":

    # Handle arguments
    args = parser.parse_args()
    forwarder = args.forwarder
    topicID = args.topicID
    test_file = args.test_file
    verbosity = args.verbosity
    transport = args.transport
    loglocally = args.log_locally
    [port, baud] = args.port.split(':')

    if verbosity >= 1:
        print "Arguments:"
        arguments = vars(args)
        for key, value in arguments.iteritems():
            print "\t%s:\t\t%s" % (key,str(value))

    # Create the publisher. 
    p = publisher(topic = topicID ,forwarderIP = forwarder)
    p.verbosity = verbosity

    # Override various functions based on the passed arguments.
    if test_file:
        p.get_data = p.get_test_data
        try:
            TESTFILE = open(test_file,'r')
        except:
            sys.exit("Error openning test file %s" % test_file)
    elif port:
        p.get_data = p.get_serial_data
        # open and configure serial port here.
        serialport = ser.Serial(port = port, baudrate = baud)
	try:
	    serialport.open()
	except:
	    print "Failed to open serial port (%s)" % port	        
        

        
    # Run it.
    try:
        p.run()
    except KeyboardInterrupt, e:
        print e
        print "Cleaning up"
        TESTFILE.close()
        
