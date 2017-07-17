from Crypto.Hash import SHA256

def RSA_sign(sk,code):
    '''Uses the RSA secret key sk to return a signature (as a string) for the string code.
    
    Preconditions: sk is an RSA secret key, code is a string'''
    
    code = code.encode('utf-8')
    
    hash = SHA256.new(code).digest()
    signature = sk.sign(hash,'')
    return str(signature[0])

def RSA_verify(pk,code,sig):
    '''Returns True if sig is a valid signature for code when signed by the counterpart
    to the RSA public key object pk.
    
    Preconditions: pk is an RSA public key, code and sig are strings'''
    
    sig = int(sig)
    sig = (sig,)  #for some reason, sig needs to be a tuple
    code = code.encode('utf-8')
    
    hash = SHA256.new(code).digest()
    return pk.verify(hash,sig)