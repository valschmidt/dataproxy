#!/usr/bin/env python
#
# Val Schmidt
# Center for Coastal and Ocean Mapping
# Univeristy of New Hampshire
# Copyright 2016

import _mypath
import dataproxy
import time
import datetime as dt
import sys

# Set up argument parsing
import argparse
parser = argparse.ArgumentParser()
#group = parser.add_mutually_exclusive_group()
parser.add_argument("-f","--forwarder",
                    action = "store",
                    default = "marvel.ccom.unh.edu",
                    help = "IP address or DNS name of the forwarder")
parser.add_argument("-t","--topicID",
                    action = "store",
                    default = "",
                    help = "Optional text subscription topic. Default subscribes to everything.")
parser.add_argument("-d","--datatype",
                   action = "store",
                   default = "s",
                   choices = ["s","i","b"],
                   help = "Type of data sent. One of string(s), jpg image(i), binary blob(b)")
parser.add_argument("-T","--transport",
                    action = "store",
                    choices = ["s","p","b","zb","n"],
                    default = "s",
                    help = "Set transport method: string, compressed pickle, binary, compressed binary, numpy")
parser.add_argument("-l","--log_locally",
                    action = "store_true",
                    default = False,
                    help = "Log images locally [NOT IMPLEMENTED]")
parser.add_argument("-v","--verbosity",
                    action = "count",
                    help = "Verbose output to terminal")

class subscriber(dataproxy.subscriber):

    def process_data(self,data):
        print "Received[%s]: %s" % (dt.datetime.now().isoformat(),data.rstrip())
        return

    def assign_receiver(self,argument):
        ''' 
        A utility method to assign the appropriate receive function.

        This works like a switch:case statement in other languages.
        See: http://www.pydanny.com/why-doesnt-python-have-switch-case.html
        '''
        switcher = {
            "s":self.recv_string,
            "p":self.recv_zipped_pickle,
            "b":self.recv_zipped_binary,
            "n":self.recv_array,
            }
        return switcher.get(argument, "")

if __name__ == "__main__":
 
    # Handle arguments
    args = parser.parse_args()
    forwarder = args.forwarder
    topicID = args.topicID
    verbosity = args.verbosity
    transport = args.transport
    loglocally = args.log_locally

    # Print the arguments
    if verbosity >= 1:
        print "Arguments:"
        arguments = vars(args)
        for key, value in arguments.iteritems():
            print "\t%s:\t\t%s" % (key,str(value))

    # Create the subscriber
    s = subscriber(forwarderIP = forwarder,topicfilter = topicID)
    s.verbosity = verbosity

    # Set up the subscriber
    s.recv = s.assign_receiver(transport)
    
    # Run it.
    try:
        s.run()
    except KeyboardInterrupt, e:
        print e
        print "Cleaning up."
        # Close all logs
