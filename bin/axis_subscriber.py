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
import os
from shutil import copyfile
#import Image
#from cStringIO import StringIO
#import Tk, ImageTk

# Set up argument parsing
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-f","--forwarder",
                    action = "store",
                    default = "localhost",
                    help = "IP address or DNS name of the forwarder")
parser.add_argument("-i","--topicID",
                    action = "store",
                    default = "TEST_123",
                    help = "Text string for ID of this published topic.")
parser.add_argument("-d","--log_dir",
                    action = "store",
                    default = ".",
                    help = "Log images to directory")
parser.add_argument("-v","--verbosity",
                    action = "count",
                    help = "Verbose output to terminal")

global log_dir
log_dir = "."

class subscriber(dataproxy.subscriber):

    def process_data(self,data):
        # The axis camera will send jpg images. For now we simply capture them and write them to disk.
        #im = Image(StringIO(data.read()))
        global log_dir
        
        #filename = os.path.join(log_dir,'image_%02d.jpg' % dt.datetime.now().second)
        filename = os.path.join(log_dir,'image_%d.jpg' % int(time.time()))
        fh = open(filename,'w')
        fh.write(data)
        fh.close()
        copyfile(filename,os.path.join(log_dir,'latest.jpg'))
        return

if __name__ == "__main__":

    # Handle arguments
    args = parser.parse_args()
    forwarder = args.forwarder
    topicID = args.topicID
    log_dir = args.log_dir
    verbosity = args.verbosity

    s = subscriber(forwarderIP = forwarder,topicfilter = topicID)
    s.run()
