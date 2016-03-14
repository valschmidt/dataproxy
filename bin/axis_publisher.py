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
import urllib2


axisip = '192.168.8.96'

# Set up argument parsing.
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-f","--forwarder", 
                    action = "store",
                    default = "marvel.ccom.unh.eduu",
                    help = "IP address or DNS name of the forwarder")
parser.add_argument("-a","--axis_camera", 
                    action = "store",
                    default = axisip,
                    help = "IP address or DNS name of the axis camera")
parser.add_argument("-l","--log_locally",
                    action = "store_true",
                    default = False,
                    help = "Log images locally [NOT IMPLEMENTED]")
parser.add_argument("-v","--verbosity",
                    action = "count",
                    help = "Verbose output to terminal")


class publisher(dataproxy.publisher):

    def get_data(self):
        time.sleep(1)
        url = "http://%s/axis-cgi/jpg/image.cgi" % axisip

        try:
            I = urllib2.urlopen(url)
        except:
            print "Error getting image at %s" % url
            return ""

        print "Sending image..."
        return I.read()

if __name__ == "__main__":

    args = parser.parse_args()
    
    forwarder = args.forwarder
    axisip = args.axis_camera
    verbosity = args.verbosity
    loglocally = args.log_locally

#     if sys.argv.__len__() > 1:
#         forwarder = sys.argv[1]
#     else:
#         forwarder = "localhost"
    print "Sending to forwarder %s:" % forwarder

    p = publisher(topic = "TEST 123",forwarderIP = forwarder)
    try:
        p.run()
    except KeyboardInterrupt, e:
        print e
        print "Cleaning up"
        
        
