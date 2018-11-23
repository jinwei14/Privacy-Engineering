import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)

while True:
    msg = socket.recv()
    print (msg)
    socket.send(str(bin(888)).encode('utf8'))
    # socket.send(b"client message to server2")
    time.sleep(1)