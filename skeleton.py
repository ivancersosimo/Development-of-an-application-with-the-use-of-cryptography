import sys
import hmac
from hashlib import md5

def gen_symk(randomness):
	#generate key
	return symk

def gen_asymkpair(randomness):
	#generate keypair
	return pub, secret



def symmetric_enc(data):
	# use a library for symmetric encryption


	return enc_data


def asymmetric_enc(data):
	# use a library for symmetric encryption


	return enc_data

def encode_output(encrypted_data):
	# encode output
	return encoded_enc_data


def hmac(key, msg):
    return hmac.HMAC(key, msg, md5)

def main():

	if len(sys.argv) < 2:
		print('provide an input file')
		exit(1)
	

main()