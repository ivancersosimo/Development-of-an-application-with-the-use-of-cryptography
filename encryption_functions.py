from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import pyminizip as pyzip
from Crypto.Hash import HMAC, SHA256

def gen_symk(randomness):
    symk = get_random_bytes(randomness)
    return symk

def symmetric_enc(data):
    # use a library for symmetric encryption
    key = gen_symk(16) # save the key or get lost
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    out = []
    out.append(cipher.nonce)
    out.append(ciphertext)
    out.append(key)
    out.append(tag)
    return out # save the tag or get lost

def symmetric_dec(dataEncrypted):
    #key is in the data, take it in variable key, same with tag and same with nonce
    cipher = AES.new(key,AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(dataEncrypted,tag)
    return data