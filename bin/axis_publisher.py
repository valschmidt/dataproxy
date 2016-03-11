#!/usr/bin/env python
#
# Val Schmidt
# Center for Coastal and Ocean Mapping
# Univeristy of New Hampshire
# Copyright 2016

import dataproxy
import time
import sys
import urllib2

axisip = 192.168.8.96


class publisher(dataproxy.publisher):

    def get_data(self):
        time.sleep(1)
        url = "http://%s/axis-cgi/jpg/image.cgi" % axisip
        
        try:
            I = urllib2.open(url)
        except:
            print "Error getting image at %s", url

        print "Sending image..."
        return I

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
        
