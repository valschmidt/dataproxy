#!/usr/bin/type python
#
# Val Schmidt
# Center for Coastal and Ocean Mapping
# University of New Hampshire
# Copyright 2016

import zmq
import sys
import datetime as dt
import time
import zlib, CPickle as pickle

# import logging   // Set up logging. 

class forwarder:
    '''
    A class to create a zmq message proxy.
    '''

    def __init__(self, in_port=7777, out_port = 7778):
    	self.data = ""
        self.in_port = in_port
        self.out_port = out_port
	pass
        
    def run(self):
        try:
            context = zmq.Context(1)
            # Socket facing clients
            frontend = context.socket(zmq.SUB)
            frontend.bind("tcp://*:%s" % self.in_port)
            
            frontend.setsockopt(zmq.SUBSCRIBE, "")
            
            # Socket facing services
            backend = context.socket(zmq.PUB)
            backend.bind("tcp://*:%s" % self.out_port)

            zmq.device(zmq.FORWARDER, frontend, backend)
        except (KeyboardInterrupt,Exception) as e:
            print e
            print "bringing down zmq device"
        finally:
            pass
            frontend.close()
            backend.close()
            context.term()

class publisher:
    '''
    A class to publish data to the data proxy forwarder.
    '''
    def __init__(self,topic, forwarderIP, out_port = 7777):
        self.topic = topic
        self.forwarderIP = forwarderIP
        self.out_port = out_port
        pass
        
    def get_data(self):
        '''
        A method that must be over-ridden at runtime, returning a topic 
        and string to publish.
		
        Note: get_data() must block until data is available.  
        '''
        time.sleep(1)  # 1 sec.
		
        return dt.datetime.now().isoformat() 

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.connect("tcp://%s:%s" % (self.forwarderIP, self.out_port))
        while True:
            socket.send("%s %s" % (self.topic, self.get_data()))

    def send_zipped_pickle(socket, obj, flags=0, protocol=-1):
        """pickle an object, and zip the pickle before sending it"""
        p = pickle.dumps(obj, protocol)
        z = zlib.compress(p)
        return socket.send(z, flags=flags)

    def send_array(socket, A, flags=0, copy=True, track=False):
        """send a numpy array with metadata"""
        md = dict(
            dtype = str(A.dtype),
            shape = A.shape,
        )
        socket.send_json(md, flags|zmq.SNDMORE)
        return socket.send(A, flags, copy=copy, track=track)


class subscriber:
    '''
    A class to subscribe to data from the data proxy forwarder.
    '''
    def __init__(self,forwarderIP, in_port = 7778, topicfilter = ""):
        self.forwarderIP = forwarderIP
        self.in_port = in_port
        self.topicfilter = topicfilter
        self.data = ""

    def process_data(self,data):
        '''
        A method to process incoming data.
        '''
        self.data = data
        
        print "Received: %s" % self.data
        return

    def recv_zipped_pickle(socket, flags=0, protocol=-1):
        """inverse of send_zipped_pickle"""
        z = socket.recv(flags)
        p = zlib.decompress(z)
        return pickle.loads(p)

    def recv_array(socket, flags=0, copy=True, track=False):
        """recv a numpy array"""
        md = socket.recv_json(flags=flags)
        msg = socket.recv(flags=flags, copy=copy, track=track)
        buf = buffer(msg)
        A = numpy.frombuffer(buf, dtype=md['dtype'])
        return A.reshape(md['shape'])

		
    def run(self):
		
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        print "Collecting updates from server (%s)..." % self.forwarderIP
        socket.connect ("tcp://%s:%s" % (self.forwarderIP, self.in_port))	    
        socket.setsockopt(zmq.SUBSCRIBE, self.topicfilter)

        while True:
            self.process_data(socket.recv())
