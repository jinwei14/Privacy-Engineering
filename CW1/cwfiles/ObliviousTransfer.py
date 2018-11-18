
from cryptography.fernet import Fernet

class ObliviousTransfer:
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

    """

    def __init__(self):
        self.A = None
        self.B = None

    def generatePublicPrivateKeys(self):
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

b = ObliviousTransfer()
print(b.generatePublicPrivateKeys())

