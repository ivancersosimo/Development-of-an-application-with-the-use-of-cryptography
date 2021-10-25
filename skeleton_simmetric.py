#!/usr/bin/env python3

import sys
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import pyminizip as pyzip
from optparse import OptionParser
from Crypto.Hash import HMAC, SHA256

def gen_symk(randomness):
    symk = get_random_bytes(randomness)
    return symk

def gen_asymkpair(randomness):
    #generate keypair
    return pub, secret

def asymmetric_enc(data):
    # use a library for symmetric encryption
    return enc_data

def encode(binary_data):
    # encode output
    return base64.b64encode(binary_data)

def saveout(ciphertext, key, extra=None):

    compression = 8
    password = input('Type a password to protect your files\n')
    with open("/tmp/ctext", "wb") as ctext:
        ctext.write(ciphertext)
        ctext.close
    with open("/tmp/key", "w") as fkey:
        fkey.write("bb")
        fkey.close
    with open("/tmp/extra", "w") as fextra:
        fextra.write("cc")
        fextra.close
    # tmp filename, buffer, name of zip, password, compression level
    pyzip.compress("/tmp/ctext",ciphertext, "ciphertext.zip", "", compression)
    pyzip.compress("/tmp/key", key, "key.zip", password, compression)
    pyzip.compress("/tmp/extra",extra, "extra_cipher.zip", password, compression)
    
    return

def symmetric_dec(data):
    pass


def symmetric_enc(data):
    # use a library for symmetric encryption
    key = gen_symk(16) # save the key or get lost
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    out = []
    out.append(ciphertext)
    out.append(key)
    out.append(tag)
    return out # save the tag or get lost

def verifyMessege(Hash, key, msg):
    try:
        Hash.hexverify(msg)
        print("The message '%s' is authentic" % msg)
    except ValueError:
        print("The message or the key is wrong")

def createHmac(key):
    return HMAC.new(key, digestmod=SHA256)