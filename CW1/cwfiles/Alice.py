import util
import zmq
import random
import sys
import time
RSA_bits = 512

class Alice:

    # message is the message that alice send to bob, t is the number of message that bob can learn
    def __init__(self):
        self.ClientSocket = util.ClientSocket


    def send(self,msg):
        self.ClientSocket.send(msg)


    def receive(self):
        self.ClientSocket.receive()







port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)
print('client alice connected')

while True:
    G_sender = util.PrimeGroup()
    c = G_sender.rand_int()
    print(type(c))
    print('c is ', c)
    socket.send(str(c).encode('utf8'))

    msg = socket.recv()
    print(msg.decode())



    time.sleep(1)





