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
import zlib, cPickle as pickle

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
        self.send = ""
        self.verbosity = 0
        pass
        
    def get_data(self):
        '''
        A method that must be over-ridden at runtime, returning a topic 
        and string to publish.
		
        Note: get_data() must block until data is available.  
        '''
        time.sleep(1)  # 1 sec.
		
        return dt.datetime.now().isoformat() 

    def get_test_data(self):
        '''
        A method to publish ASCII text data, one line at a time at 1Hz from a text file.
        
        Not yet implemented
        '''
        pass
        
        

    def send_string(self,socket,msg):
        if self.verbosity >=2:
            print "Sending %s %s" % (self.topic,msg.rstrip())
        return socket.send_multipart([self.topic,msg],flags=0) 

    def send_zipped_pickle(self, socket, obj):
        """pickle an object, and zip the pickle before sending it"""
        flags=0
        protocol=-1
        p = pickle.dumps(obj, protocol)
        z = zlib.compress(p)
        return socket.send_multipart([self.topic,z],flags=flags)

    def send_zipped_binary(self,socket,buf):
        '''Send a zipped binary buffer of data.'''
        flags=0
        z = zlib.compress(buf)
        return socket.send_multipart([self.topic,z],flags=flags)

    def send_array(self,socket, A):
        """send a numpy array with metadata"""
        flags=0
        copy=True
        track=False
        md = dict(
            dtype = str(A.dtype),
            shape = A.shape,
        )
        socket.send_json(md, flags|zmq.SNDMORE)
        return socket.send(A, flags, copy=copy, track=track)

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        url = "tcp://%s:%s" % (self.forwarderIP, self.out_port)
        if self.verbosity >= 1:
            print "Connecting to %s" % url
        socket.connect(url)
        self.send = ""
        if self.send == "":
            self.send = self.send_string
            
        while True:
            self.send(socket,self.get_data())



class subscriber:
    '''
    A class to subscribe to data from the data proxy forwarder.
    '''
    def __init__(self,forwarderIP, in_port = 7778, topicfilter = ""):
        self.forwarderIP = forwarderIP
        self.in_port = in_port
        self.topicfilter = topicfilter
        self.data = ""
        self.recv = ""
        self.verbosity = 0

    def process_data(self,data):
        '''
        A method to process incoming data.
        '''
        self.data = data
        
        print "Received: %s" % self.data
        return

    def recv_string(self,socket):
        [address, data] = socket.recv_multipart()
        return data 

    def recv_zipped_pickle(self,socket):
        """inverse of send_zipped_pickle"""
        flags=0
        protocol = -1
        #z = socket.recv(flags)
        [address, z] = socket.recv_multipart()
        p = zlib.decompress(z)
        return pickle.loads(p)

    def recv_zipped_binary(self,socket):
        flags=0
        [address,z] = socket.recv_multipart()
        p = zlib.decompress(z)
        return p

    def recv_array(self,socket):
        """recv a numpy array"""
        flags=0
        copy=True, 
        track=False
        md = socket.recv_json(flags=flags)
        msg = socket.recv(flags=flags, copy=copy, track=track)
        buf = buffer(msg)
        A = numpy.frombuffer(buf, dtype=md['dtype'])
        return A.reshape(md['shape'])

		
    def run(self):
		
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        if self.verbosity >= 1:
            print "Connecting to server (%s:%s)..." % (self.forwarderIP,self.in_port)

        socket.connect ("tcp://%s:%s" % (self.forwarderIP, self.in_port))
        if self.verbosity >= 1:
            print "Subscribing to topic: %s" % self.topicfilter

        socket.setsockopt(zmq.SUBSCRIBE, self.topicfilter)

        self.recv = self.recv_string
        # Set the transmission mode
        if self.recv == "":
            self.recv = self.recv_string

        while True:
            self.process_data(self.recv(socket))

