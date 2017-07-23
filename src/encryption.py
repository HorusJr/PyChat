from Crypto.PublicKey import RSA
from Crypto import Random

def RSA_encrypt(pk,message):
    '''Encrypts the string message with the public key pk.
    
    Preconditions: pk is an RSA public-key object, message is a string with size up to than 128 bytes'''
    
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
    #to send the public key information to the server, extract the information
    #with pk.n and pk.e
    
    #to initialize a public key from n and e, use RSA.construct((n,e))
    
    random_generator = Random.new().read
    sk = RSA.generate(1024, random_generator)
    pk = sk.publickey()
    
    return [pk,sk]

def long_RSA_encrypt(pk,message):
    '''Encyrpts the string message with the public key pk.
    
    The string message may be of any size.  To acccommodate this, message will be encrypted in 128-character chunks,
    and the encrypted chunks will be concatenated and returned.
    
    Preconditions: pk is an RSA public-key object, message is a string'''
    
    #breaking the message up:
    msg_parts = []
    
    while len(message)>128:
        msg_part = message[:128]
        msg_parts.append(msg_part)
        message = message[128:]
    msg_parts.append(message)
    
    #encrypting each chunk:
    output = b''
    for msg in msg_parts:
        output = output + RSA_encrypt(pk,msg)
    
    return output

def long_RSA_decrypt(sk,message):
    '''Decrypts the string message with the public key pk.
    
    This function will decode message encrypted with either RSA_encrypt or long_RSA_encrypt
    
    Preconditions: sk is an RSA key object, message is encrypted with sk's corresponding pk'''
    
    #breaking up the message:
    msg_parts = []
    
    while len(message) != 0:
        msg_part = message[:128]
        msg_parts.append(msg_part)
        message = message[128:]
    
    #decrypting each chunk:
    output = ''
    for msg in msg_parts:
        output = output + RSA_decrypt(sk,msg)
    
    return output