import util
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







alice = Alice()
while True:
    alice.send(b'Server message to client3')
    msg = alice.recv()
    print (msg)
    time.sleep(1)





