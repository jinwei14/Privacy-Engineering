import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

while True:
    socket.send(str(123).encode('utf8'))
    msg = socket.recv()
    # msg = int.from_bytes(msg, byteorder='little')
    print (msg.decode(), 'the type is ', type(msg.decode()))
    time.sleep(1)