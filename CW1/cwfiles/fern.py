from cryptography.fernet import Fernet
import base64
import ast

"""
Submission by:
Thien Nguyen (tn518 / 01565994)
Jinwei Zhang (jz2618 / 01540854)
"""

def encryptInput(privateKey, value):
    crypt = Fernet(privateKey)
    message = str(value).encode('utf-8')
    encryptedValue = crypt.encrypt(message)
    # return encode(encryptedValue)
    return encryptedValue

def decryptInput(privateKey, token):
    crypt = Fernet(privateKey)
    return crypt.decrypt(token)

def binaryXOR(x,y):
    if x == y:
        return 0
    return 1
    
def encode(token):
    return ["{0:b}".format(i) for i in token]

def XOR(encryptedToken, p=1):
    xoredTokenBits = []
    for i in encryptedToken:
        binary = i
        newBinary = [binaryXOR(int(binary[j]),p) for j in range(len(binary))]
        newBinary = ''.join(str(i) for i in newBinary)
        xoredTokenBits.append(newBinary)
    return xoredTokenBits
    
def decode(ku):
    ku = [int(m, 2) for m in ku]
    ku = "".join(map(chr, ku))
    return  ku.encode('utf-8')

def toString(ku):
    return str(ku)

def stringToList(ku):
    return ast.literal_eval(ku)

if __name__ == "__main__":
    """
    Used for testing purposes.
    """

    key = Fernet.generate_key()
    f = Fernet(key)
 
    
    inp = '0'
    print()
    print("INPUT    :",inp)
    token = f.encrypt(inp.encode('utf-8'))
    print("ENCRYPTED:",token)
    print(f.encrypt(inp.encode('utf-8')))

    decrp = f.decrypt(token)

    print("DECRYPTED:",decrp.decode('utf-8'))
    print()
