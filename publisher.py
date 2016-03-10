#!/usr/bin/env python
#
# Val Schmidt
# Center for Coastal and Ocean Mapping
# Univeristy of New Hampshire
# Copyright 2016

import dataproxy
import time
import sys

GPSFILE = open("test/HLY0805-posnav.y2008d233",'r')

class publisher(dataproxy.publisher):

    def get_data(self):
        time.sleep(1)
        line = GPSFILE.readline()
        # Restart at the beginning if we get to the end.
        if line == "":
            GPSFILE.seek(0)
            line = GPSFILE.readline()

        print "Sending: " + line.rstrip()
        return line

if __name__ == "__main__":

    if sys.argv.__len__() > 1:
        forwarder = sys.argv[1]
    else:
        forwarder = "localhost"
    print "Sending to forwarder %s:" % forwarder

    p = publisher(topic = "TEST 123",forwarderIP = forwarder)
    try:
        p.run()
    except KeyboardInterrupt, e:
        print e
        print "Cleaning up"
        GPSFILE.close()
        
