import pyDes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto import Random
import binascii
import time
from matplotlib import pyplot as plt
import numpy as np
import sys

#----- Symmetric encryption --------
# DES

data = "DES Algorithm Implementation"

def des_encryption(message):
    k = pyDes.des("DESCRYPT", pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    encrypted = k.encrypt(message)

    #print("Encrypted: {}".format(d))
    #print("Decrypted: {}".format(k.decrypt(d)))

    return encrypted


# AES 256
#https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
def aes_encryption(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message)

    return ciphertext



#----- Asymmetric encryption -----
# RSA-OAEP (Optimal Asymmetric Encryption Padding)
# https://cryptobook.nakov.com/asymmetric-key-ciphers/rsa-encrypt-decrypt-examples


def rsa_encryption(message, publicKey):

    #pubKey = keypair.publickey()
    #print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
    #pubKeyPEM = pubKey.exportKey()
    #print(pubKeyPEM.decode('ascii'))

    #print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")
    #privKeyPEM = keypair.exportKey()
    #print(privKeyPEM.decode('ascii'))

    #privKkeyPEM = keypair.exportKey()
    encryptor = PKCS1_OAEP.new(publicKey)
    encrypted = encryptor.encrypt(message)

    return encrypted

    #print("Encrypted: ", binascii.hexlify(encrypted))

def rsa_decryption(encrypted_message, keypair):
    decryptor = PKCS1_OAEP.new(keypair)
    decrypted = decryptor.decrypt(encrypted_message)

    print('Decrypted: ', decrypted)


def plot_diagram(size_values, rsa_values, aes_values):
    plt.plot(size_values, rsa_values, label='rsa_values')
    plt.plot(size_values, aes_values, label='aes_values')
    plt.xlabel("String size (Bytes)")
    plt.ylabel("Execution time (s)")
    #plt.xscale('log')
    plt.show()

def plot_diagram_aes(size_values, aes_values):
    plt.plot(size_values, aes_values, label='aes_values', color='orange')
    plt.xlabel("String size (Bytes)")
    plt.ylabel("Execution time (s)")
    plt.xscale('log')
    plt.show()



if __name__ == "__main__":

    message = b'A'

    AES_SIMPLE_KEY = b'Sixteen byte key'

    RSA_KEYPAIR = RSA.generate(2048)

    size_values = []
    time_rsa_values = []
    time_des_values = []
    time_aes_values = []

    for iteration in range(30):
        message += message
        #print(message)
        message_size_bytes = len(message)
        message_len = len(message)

        size_values.append(message_size_bytes)

        #start_rsa_time = time.time()
        #rsa_encryption(message, RSA_KEYPAIR.publickey())
        #rsa_execution_time = time.time()-start_rsa_time
        #print("RSA Encryption time: ", rsa_execution_time)
        #time_rsa_values.append(rsa_execution_time/1000)
        #time_rsa_values.append(rsa_execution_time)


        start_aes_time = time.time()
        aes_encryption(message, AES_SIMPLE_KEY)
        aes_execution_time = time.time()-start_aes_time
        time_aes_values.append(aes_execution_time)

        #start_des_time = time.time()
        #des_encryption(message)
        #des_execution_time = time.time()-start_des_time
        #print("DES Encryption time: ", des_execution_time)

        """print("Iteration: {}\nSize: {}\nRSA time: {}\nAES time: {}\nDES time: {}".format(
            iteration, message_size_bytes, 
            0, aes_execution_time, 0
        ))"""

        #print(len(size_values), len(time_rsa_values), len(time_aes_values))
        print(message_size_bytes)

    #plot_diagram(size_values, time_rsa_values, time_aes_values)
    plot_diagram_aes(size_values, time_aes_values)
