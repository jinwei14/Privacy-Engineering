import util
RSA_bits = 512
import time

class Bob:

    # message is the message that alice send to bob, t is the number of message that bob can learn
    def __init__(self):
        self.ServerSocket = util.ServerSocket()

    def send(self, msg):
        self.ServerSocket.send(msg)

    def receive(self):
        self.ServerSocket.receive()








import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
print('bob listening')
socket.bind("tcp://*:%s" % port)
print('server bob connected')

while True:

    msg = socket.recv()
    print (msg)
    socket.send(b'Server message to client3')
    time.sleep(1)



print('hah')