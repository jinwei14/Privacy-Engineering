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
    print (msg.decode())
    c= int(msg.decode())

    G_rece = util.PrimeGroup()
    x = G_rece.primeM1
    print(type(x))
    print('x is ', x)

    g = G_rece.find_generator()
    print(type(g))
    print('g is ', g)

    h_b = pow(g, x, 2)
    h_1b = c // h_b
    print(type(h_b), type(h_1b))
    print('h_b is ', h_b, 'h_1b is ', h_1b)
    # h0 (h_1b) is send to sender
    socket.send(str(h_1b).encode('utf8'))

    
    time.sleep(1)



print('hah')