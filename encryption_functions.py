from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import pyminizip as pyzip
from Crypto.Hash import HMAC, SHA256
import ast
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from nacl.signing import VerifyKey
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

def performHash(data):
    hash_object = SHA256.new(str(data).encode("utf-8"))
    hash_val = hash_object.hexdigest()
    return hash_val

def signerPersp(nsMessege):
    print("# Generate a new random signing key")
    signing_key = SigningKey.generate()

    print("# Sign a message with the signing key")
    signed_hex = signing_key.sign(nsMessege, encoder=HexEncoder)

    print("# Obtain the verify key for a given signing key")
    verify_key = signing_key.verify_key

    print("# Serialize the verify key to send it to a third party")
    verify_key_hex = verify_key.encode(encoder=HexEncoder)
    output = [signed_hex, verify_key_hex]
    print(signed_hex)

    return output
    
def veryfierPersp(signed_hex, verify_key_hex):
    print(" # Create a VerifyKey object from a hex serialized public key")
    verify_key = VerifyKey(verify_key_hex, encoder=HexEncoder)
    print(signed_hex)
    print( " # Check the validity of a message's signature # The message and the signature can either be passed together, or # separately if the signature is decoded to raw bytes.  These are equivalent:")
    verify_key.verify(signed_hex, encoder=HexEncoder)
    print("here")

    signature_bytes = HexEncoder.decode(signed_hex.signature)
    verify_key.verify(signed_hex.message, signature_bytes,
                    encoder=HexEncoder)

    # Alter the signed message text
    forged = signed_hex[:-1] + bytes([int(signed_hex[-1]) ^ 1])
    # Will raise nacl.exceptions.BadSignatureError, since the signature check
    # is failing
    verify_key.verify(forged)