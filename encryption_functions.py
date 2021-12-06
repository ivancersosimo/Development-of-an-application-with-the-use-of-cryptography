from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
import base64
import pyminizip as pyzip
from Crypto.Hash import HMAC, SHA256
import ast
from Crypto.PublicKey import RSA
import Crypto.IO.PEM as pem
from Crypto.Signature import pkcs1_15

def gen_symk(randomness):
    symk = get_random_bytes(randomness)
    return symk

def symmetric_enc(data):
    # use a library for symmetric encryption
    key = gen_symk(16) # save the key or get lost
    cipher = AES.new(key, AES.MODE_EAX)
    data = str(data).encode("utf-8")
    ciphertext, tag = cipher.encrypt_and_digest(data)
    out = []
    out.append(cipher.nonce)
    out.append(ciphertext)
    out.append(key)
    out.append(tag)
    return out # save the tag or get lost

def symmetric_dec(dataEncrypted):
    nonce = dataEncrypted[0]
    ciphertext = dataEncrypted[1]
    key = dataEncrypted[2]
    tag = dataEncrypted[3]
    cipher = AES.new(key,AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext,tag).decode("utf-8")
    data = ast.literal_eval(data)
    return data

def asymmetric_enc(data,pubkey_path):
    pbk = pem.decode(open(pubkey_path,"r").read(), passphrase="1234".encode('utf-8'))
    pubkey = RSA.import_key(pbk[0])
    cipher_rsa = PKCS1_OAEP.new(pubkey)
    data_key = str(data[2]).encode('utf-8')
    dataEncrypted_key = cipher_rsa.encrypt(data_key)
    return [data[0],data[1], dataEncrypted_key, data[3]]
    
def asymmetric_dec(dataEncrypted,privkey_path):
    pvk =pem.decode(open(privkey_path,"r").read(), passphrase="1234".encode('utf-8'))
    privkey = RSA.import_key(pvk[0])
    cipher_rsa = PKCS1_OAEP.new(privkey)
    dataEncrypted_key = dataEncrypted[2]
    data = cipher_rsa.decrypt(dataEncrypted_key).decode("utf-8")
    data = ast.literal_eval(data)
    return [dataEncrypted[0], dataEncrypted[1], data, dataEncrypted[3]]

def performHash(data):
    hash_object = SHA256.new(str(data).encode("utf-8"))
    hash_val = hash_object.hexdigest()
    return hash_val

def signMessage(dataEncrypted,privk_path, database=False):
    if database == False:
        message = dataEncrypted[0] + dataEncrypted[1] + dataEncrypted[2] + dataEncrypted[3]
    elif database == True:
        message = str(dataEncrypted).encode("utf-8")
    pvk = pem.decode(open(privk_path, "r").read(), passphrase = "1234".encode("utf-8"))
    key = RSA.import_key(pvk[0])
    h = SHA256.new(message)
    h.hexdigest()
    signature = pkcs1_15.new(key).sign(h)
    return signature

def verifySignature(dataEncrypted,signature,pubkey_path,datab = False):
    if datab==False:
        message = dataEncrypted[0] + dataEncrypted[1] + dataEncrypted[2] + dataEncrypted[3]
    elif datab ==True:
        message = str(dataEncrypted).encode("utf-8")
    pbk = pem.decode(open(pubkey_path, "r").read(),passphrase = "1234".encode("utf-8"))
    key = RSA.import_key(pbk[0])
    h = SHA256.new(message)
    try:
        pkcs1_15.new(key).verify(h,signature)
        verification = True
    except:
        return False
    return verification