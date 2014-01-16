from Crypto.Random import random
from Crypto.Hash import SHA, SHA256
from Crypto import Random
from Crypto.PublicKey import RSA

class KeyGen:

    # generate an RSA key pair
    @staticmethod
    def generate_rsa_key():
        rand_gen = Random.new().read
        k = RSA.generate(1024, rand_gen)
        return k

    # generate 32-byte AES secret key
    @staticmethod
    def generate_aes_key():
        # hash a random 256-bit long integer
        rand_nbr = random.getrandbits(256)
        sha = SHA256.new(str(rand_nbr))
        k = sha.digest()
        return k

    # generate a user-friendly recovery key
    @staticmethod
    def generate_recovery_key():
        # hash a random 256-bit long integer
        rand_nbr = random.getrandbits(256)
        sha = SHA.new(str(rand_nbr))
        # get the hex digest (40 alphanumeric characters)
        k = sha.hexdigest()
        # take the first 25 characters and upper case them
        k = k[:25].upper()
        # now insert hyphens for readability
        k = '%s-%s-%s-%s-%s' % (k[:5],k[5:10],k[10:15],k[15:20],k[20:])
        return k