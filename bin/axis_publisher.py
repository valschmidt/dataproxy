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
                    default = "localhost",
                    help = "IP address or DNS name of the forwarder")
parser.add_argument("-a","--axis_camera", 
                    action = "store",
                    default = axisip,
                    help = "IP address or DNS name of the axis camera")
parser.add_argument("-i","--topicID",
                    action = "store",
                    default = "CAMERA_01",
                    help = "Text string for ID of this published topic.")
parser.add_argument("-d","--delay",
                    action = "store",
                    default = 1,
                    type = float,
                    help = "Time in seconds to delay before sending the next image.")
parser.add_argument("-l","--log_locally",
                    action = "store_true",
                    default = False,
                    help = "Log images locally [NOT IMPLEMENTED]")
parser.add_argument("-v","--verbosity",
                    action = "count",
                    help = "Verbose output to terminal")


class publisher(dataproxy.publisher):

    def get_data(self):
        time.sleep(delaysecs)
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
    topicID = args.topicID
    delaysecs = args.delay
    verbosity = args.verbosity
    loglocally = args.log_locally

    if verbosity >= 1:
        print "Arguments:"
        arguments = vars(args)
        for key, value in arguments.iteritems():
            print "\t%s:\t\t%s" % (key,str(value))

    p = publisher(topic = topicID,forwarderIP = forwarder)
    try:
        p.run()
    except KeyboardInterrupt, e:
        print e
        print "Cleaning up"
        
        
