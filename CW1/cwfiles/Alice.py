import rsa
RSA_bits = 512

class Alice:

    # message is the message that alice send to bob, t is the number of message that bob can learn
    def __init__(self, message, t):
        self.message = message
        self.t = t
        (pubkey1, privkey1) = self.generateKeyPairs()
        (pubkey2, privkey2) = self.generateKeyPairs()






    def generateKeyPairs(self):

        return 0


    def sendMessage(self):

        # send all of this.
        return self.message


    #once alice receiced the EncrtptedKey alice decript it using it private keys
    def receivedEncrtptedKey(self, EncrtptedKey):
        # key1 =
        # key2 =

        return 0;








