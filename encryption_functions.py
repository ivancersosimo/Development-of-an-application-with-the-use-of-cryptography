from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
import base64
import pyminizip as pyzip
from Crypto.Hash import HMAC, SHA256
import ast
from Crypto.PublicKey import RSA
import Crypto.IO.PEM as pem

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
    pubkey = RSA.import_key(pbk)
    cipher_rsa = PKCS1_OAEP.new(pubkey)
    dataEncrypted = cipher_rsa.encrypt(data)
    return dataEncrypted
    
def asymmetric_dec(dataEncrypted,privkey_path):
    pvk =pem.decode(open(privkey_path,"r").read(), passphrase="1234".encode('utf-8'))
    privkey = RSA.import_key(pvk)
    cipher_rsa = PKCS1_OAEP.new(privkey)
    data = cipher_rsa.decrypt(dataEncrypted)
    return data

def performHash(data):
    hash_object = SHA256.new(str(data).encode("utf-8"))
    hash_val = hash_object.hexdigest()
    return hash_val