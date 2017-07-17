from Crypto.PublicKey import RSA
from Crypto import Random

def RSA_encrypt(pk,message):
    '''Encrypts the string message with the public key pk.
    
    Preconditions: pk is an RSA public-key object, message is a string with size less than 128 bytes'''
    
    if type(message) == str:
        message = message.encode('utf-8')           #RSA can only encrypt bytes
    
    encrypted = pk.encrypt(message,32)
    return encrypted[0]


def RSA_decrypt(sk,message):
    '''Decrypts the encrypted message with the secret key sk.
    
    Preconditions: message is encrypted with the public key corresponding to sk, sk is an RSA key object'''
    
    decrypted = sk.decrypt(message)
    decrypted = decrypted.decode()                    #makes decrypted a string instead of bytes
    return decrypted

def generate_RSA_keypair():
    '''Generates an RSA public/secret key pair and returns a list [pk,sk]'''
    
    random_generator = Random.new().read
    sk = RSA.generate(1024, random_generator)
    pk = sk.publickey()
    
    return [pk,sk]