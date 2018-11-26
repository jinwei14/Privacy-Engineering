import util
import math
import numpy as np
from decimal import Decimal


#---------------------------------------------------------------------------
class Alice:
    def __init__(self,msg1,msg2):
        # sender generate a prime Group
        self.G_sender = util.PrimeGroup()
        # two message that needs to be sent
        self.msg1 = msg1
        self.msg2 = msg2

    def send_c(self):
        # c -> random element in G  
        #G_sender = util.PrimeGroup() # this need to be changed to self.
        self.c = self.G_sender.rand_int()
        return self.c

    def sendMessage(self, h0):
        # h0 (h_1b) is send to sender
        h_0 = h0
        h_1 = self.G_sender.mul(self.c, self.G_sender.inv(h_0))
        k = self.G_sender.primeM1
        # g is a generator of cyclic finite abelian group G of prime order q.
        # c_1 = g**k
        c_1 = self.G_sender.gen_pow(k)
        # msg1 = self.msg1.encode()  ## this should be your input message
        # msg2 = self.msg2.encode()
        msg1 = self.msg1
        msg2 = self.msg2
        msg_length = len(self.msg1)
        # encrypt the message
        e_0 = util.xor_bytes(msg1, util.ot_hash(self.G_sender.pow(h_0, k), msg_length))
        e_1 = util.xor_bytes(msg2, util.ot_hash(self.G_sender.pow(h_1, k), msg_length))
        # send encrypted message e0 e1 and c1 to the receiver
        return c_1, [e_0, e_1],msg_length

class Bob:
    def __init__(self, choice):
        # initialise the bob with his choice 
        self.G_rece = util.PrimeGroup()
        self.x = self.G_rece.primeM1
        self.choice = choice

    def send_h0(self, c):
        #G_rece = util.PrimeGroup()
        # g is a generator of cyclic finite abelian group G of prime order q.
        g = self.G_rece.find_generator()
        # calcute the h_b and h_1b which need send to bob
        h_b = self.G_rece.gen_pow(self.x)
        h_1b = self.G_rece.mul(c, self.G_rece.inv(h_b))
        
        #send h value depends on his choice 
        if self.choice == 0:
            return h_b
        else:
            return h_1b

    def getMessage(self, c_1, encryMsg, msg_length):
        #get the encrypted message and decrypt it
        trueMessage = util.xor_bytes(encryMsg[self.choice], util.ot_hash(pow(c_1, self.x, 2), msg_length))
        return trueMessage

def test():
    bob = Bob(1)
    alice = Alice(b'Tian is cool', b'Jinn is cool')

    c = alice.send_c()
    h0 = bob.send_h0(c)

    c_1, E, length = alice.sendMessage(h0)

    trueMsg = bob.getMessage(c_1,E, length)

    # str = unicode(str, errors='replace')

    print(trueMsg.decode())



if __name__ == "__main__":
    for i in range(10):
        test()
