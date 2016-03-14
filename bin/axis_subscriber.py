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
#import Image
#from cStringIO import StringIO
#import Tk, ImageTk

class subscriber(dataproxy.subscriber):

    def process_data(self,data):
        # The axis camera will send jpg images. For now we simply capture them and write them to disk.
        #im = Image(StringIO(data.read()))
        fh = open('image_%02d.jpg' % dt.datetime.now().second,'w')
        fh.write(data)
        fh.close()
        return

if __name__ == "__main__":
    
    if sys.argv.__len__() > 1:
        forwarder = sys.argv[1]
    else:
        forwarder = "localhost"

    s = subscriber(forwarderIP = forwarder,topicfilter = "TEST 1")
    s.run()
