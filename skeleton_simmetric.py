#!/usr/bin/env python3

import sys
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import pyminizip as pyzip
from optparse import OptionParser


def gen_symk(randomness):
    #generate key
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



def symmetric_enc(data):
    # use a library for symmetric encryption
    key = get_random_bytes(16) # save the key or get lost
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    out = []
    out.append(ciphertext)
    out.append(key)
    out.append(tag)
    return out # save the tag or get lost



    


def main():

    if len(sys.argv) < 2:
        print (sys.argv[0], " --help to see the options")
    
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", help="Input file to encrypt or decrypt", metavar="FILE")
    parser.add_option("-k", "--key", dest="key", help="Input key file", metavar="KEY")
    parser.add_option("-e", "--extra", dest="extra", help="Input key file", metavar="EXTRA")
    parser.add_option("-d", "--decrypt", dest="decrypt", default=False, help="Decrypt a file")

    (options, args) = parser.parse_args()

    if (options.decrypt):
        key = options.key
        extra = options.extra
        fname = options.filename
    else:
        cleartext = open(options.filename, "rb").read() # the file name or string that you pass through the command line
        enc_v = symmetric_enc(cleartext)
        encoded_v = []
        for e in enc_v:
            encoded_v.append(encode(e))
            #saveout(encoded_v[0], encoded_v[1], encoded_v[2])
        
        saveout(encoded_v[0],encoded_v[1],encoded_v[2])

main()
