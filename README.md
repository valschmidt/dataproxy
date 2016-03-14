# dataproxy

Dataproxy is a module and collection of scripts for passing real-time
data from various publishers to various subscribers using the zmq
library. dataproxy defines the publisher, forward and subscriber
classes with the following model:

```
PUBLISHER--\                 /----SUBSCRIBER
PUBLISHER------>FORWARDER--->-----SUBSCRIBER
PUBLISHER--/                \-----SUBSCRIBER
....                              ....
```

See:
http://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/devices/forwarder.html
for more details.

The dataproxy forwarder uses ports 7777 for collecting data from
publishers and 7778 for passing data to subscribers. 

For publishers, the idea is to monitor a data input device
(e.g. serial port) or to simply capture data with some interval and
when received publish the data to the forwarder. The publisher class
impleenets a get_data() method which must be over-ridden by the user
for one's specific scenario. The publisher.py script provided in the
module implements monitoring looping over a text file for testing or
monitoring of a serial port. In either case the readline() function is
used, blocking until \n is received. 

Several options are provided for the method of transport between
publisher and subscriber and the user must take care to match
these. The most simple is simply an ASCII string. Zipped python
pickled objects are also possible as well as zipped binary blobs and
numpy arrays (not yet tested). 

To test dataproxy try the following:

```bash
cd dataproxy
bin/forwarder.py &
bin/publisher.py -t test/test.txt &
bin/subscriber.py -vv
```
Try the `-h` flag to see the various commend line arguments. 