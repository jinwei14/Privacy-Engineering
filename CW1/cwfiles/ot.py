import util
import  math
import numpy as np
from decimal import Decimal
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018
"""
- Alice has m1,m2
- Bob will learn either m1 or m2 (but not both)
- Alice gens pub-priv key pairs (Pu1, Pr1), (Pu2,Pr2)
- Alice sends Bob Pu1, Pu2
- Bob generates symmetric key K and randomly chooses Pub1
- Bob computes c=Encrypt_Pu1(K) and sends c to Alice
- Alice computes Decrypt_Pr1(c)=K [which is the good key]
- Alice computes Decrypt_Pr2(c)=U [which is the bad key]
- Alice computes c1=Encrypt_K(m1)
- Alice computes c2=Encrypt_U(m2)
- Alice sends c1,c2 to Bob
- Bob computes D_K(c1) to get the good message m1
- Bob computes D_K(c2) to get the rubbish message.

AIM: to carry out the core operations for oblivious transfer
(generate primes, xor byte sequences,
generate variable-length cryptographic hashes,
do modular exponentiation on prime number groups)
"""


"""
things needs to be improve

power()

inverse()

bits() ??? may be length massage ??


"""
class Ot:

    OBLIVIOUS_TRANSFERS = True

    if OBLIVIOUS_TRANSFERS:
    # __________________________________________________

    # bellare-micali OT with naor and pinkas optimisations, see smart p423

    # << removed >>
        print('OBLIVIOUS_TRANSFERS executing')


    else:
    # ____________________________________________________________________

    # non oblivious transfers, not even a secure channel is used, for testing

    # << removed >>

    # __________________________________________________________________________
        print('NON OBLIVIOUS_TRANSFERS executing')


def generatePublicPrivateKeys():
    from Crypto.PublicKey import RSA
    bits = 2048
    new_key = RSA.generate(bits, e=65537)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")
    return private_key, public_key


    #
    # @staticmethod
    # def primeGen(num_bits):
    #
    #     return util.gen_prime(num_bits)
#
# key = Fernet.generate_key()
# f = Fernet(key)
# token = f.encrypt(b"A really secret message. Not for prying eyes.")



# G_sender = util.PrimeGroup()
# c = G_sender.rand_int()
# print(type(c))
# print('c is ', c)
#
#
# # c sned from sender to bob for this example b = 1
#
# G_rece = util.PrimeGroup()
# x = G_rece.primeM1
# print(type(x))
# print('x is ', x)
#
# g = G_rece.find_generator()
# print(type(g))
# print('g is ', g)
#
# h_b = pow(g, x, 2)
# h_1b = c//h_b
# print(type(h_b), type(h_1b))
# print('h_b is ', h_b, 'h_1b is ', h_1b)
#
# # h0 (h_1b) is send to sender
# h_0 = h_1b
# h_1 = c//h_0
# k = G_sender.primeM2
# c_1 =  pow(g,k,2)
# msg1 = bytes('message 1 by sender', 'utf-8')
# msg2 = bytes('message 2 by sender', 'utf-8')
# msg_length = 19
# e_0 = util.xor_bytes(msg1, util.ot_hash(pow(h_0, k, 2), msg_length))
# e_1 = util.xor_bytes(msg2, util.ot_hash(pow(h_1, k, 2), msg_length))
#
#
# #e0 e1 c1 send to receiver for this example b == 1
# m_1 =  util.xor_bytes(e_1, util.ot_hash(pow(c_1,x,2), msg_length))
# print('the messgae that bob get is ', m_1.decode('ascii'))


#---------------------------------------------------------------------------

# #
# G_sender = util.PrimeGroup()
# c = G_sender.rand_int()
# print(type(c))
# print('c is ', c)
#
#
# # c sned from sender to bob for this example b = 1
#
# G_rece = util.PrimeGroup()
# x = G_rece.primeM1
# print(type(x))
# print('x is ', x)
#
# g = G_rece.find_generator()
# print(type(g))
# print('g is ', g)
#
# h_b = G_rece.gen_pow(x)
# h_1b = G_rece.mul(c,G_rece.inv(h_b))
# print(type(h_b), type(h_1b))
# print('h_b is ', h_b, 'h_1b is ', h_1b)
#
# # h0 (h_1b) is send to sender
# h_0 = h_1b
# h_1 = G_sender.mul(c,G_sender.inv(h_0))
# k = G_sender.primeM2
# c_1 = G_sender.gen_pow(k)
# msg1 = 'message 1 by sender'.encode()
# msg2 = 'message 2 by sender'.encode()
# msg_length = 19
# e_0 = util.xor_bytes(msg1, util.ot_hash(G_sender.pow(h_0, k), msg_length))
# e_1 = util.xor_bytes(msg2, util.ot_hash(G_sender.pow(h_1, k), msg_length))
#
#
# #e0 e1 c1 send to receiver for this example b == 1
# m_1 =  util.xor_bytes(e_1, util.ot_hash(pow(c_1,x,2), msg_length))
# print('the messgae that bob get is ', m_1.decode())

#---------------------------------------------------------------------------
class Alice:
    def __init__(self):
        self.G_sender = util.PrimeGroup()

    def send_c(self):
        #G_sender = util.PrimeGroup() # this need to be changed to self.
        c = self.G_sender.rand_int()
        print(type(c))
        print('c is ', c)
        return c

    def sendMessage(self, h0, msg1, msg2):
        # h0 (h_1b) is send to sender
        h_0 = h0
        h_1 = self.G_sender.mul(c, self.G_sender.inv(h_0))
        k = self.G_sender.primeM1
        c_1 = self.G_sender.gen_pow(k)
        msg1 = msg1.encode()  ## this should be your input message
        msg2 = msg2.encode()
        msg_length = len(msg1)
        e_0 = util.xor_bytes(msg1, util.ot_hash(self.G_sender.pow(h_0, k), msg_length))
        e_1 = util.xor_bytes(msg2, util.ot_hash(self.G_sender.pow(h_1, k), msg_length))
        return c_1, [e_0, e_1],msg_length



class Bob:
    def __init__(self, choice):
        self.G_rece = util.PrimeGroup()
        self.x = self.G_rece.primeM1
        self.choice = choice

    def send_h0(self, c):
        #G_rece = util.PrimeGroup()
        print(type(self.x))
        print('x is ', self.x)

        g = self.G_rece.find_generator()
        print(type(g))
        print('g is ', g)

        h_b = self.G_rece.gen_pow(self.x)
        h_1b = self.G_rece.mul(c, self.G_rece.inv(h_b))
        print(type(h_b), type(h_1b))
        print('h_b is ', h_b, 'h_1b is ', h_1b)

        if self.choice == 0:
            return h_b
        else:
            return h_1b

    def getMessage(self, c_1, encryMsg, msg_length):
        trueMessage = util.xor_bytes(encryMsg[self.choice], util.ot_hash(pow(c_1, self.x, 2), msg_length))
        return trueMessage


bob = Bob(1)
alice = Alice()

c = alice.send_c()
h0 = bob.send_h0(c)

c_1, E, length = alice.sendMessage(h0, 'Tian is cool', 'Jinn is cool')

trueMsg = bob.getMessage(c_1,E, length)

# str = unicode(str, errors='replace')

print(trueMsg.decode())


