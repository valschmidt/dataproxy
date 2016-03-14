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

class subscriber(dataproxy.subscriber):

    def process_data(self,data):
        print "Received[%s]: %s" % (dt.datetime.now().isoformat(),data.rstrip())
        return

if __name__ == "__main__":
    
    if sys.argv.__len__() > 1:
        forwarder = sys.argv[1]
    else:
        forwarder = "localhost"

    s = subscriber(forwarderIP = forwarder,topicfilter = "TEST_123")
    s.verbosity = 2
    s.run()
