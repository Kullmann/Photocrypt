# Need to generate private and public keys for user one time
# then user passes private key in for encryption and decryption
# have to generate AES and RSA keys for user
from Cryptodome.PublicKey import RSA

key = RSA.generate(2048)
def generatePrivateKey():
    private_key = key.export_key()
    return private_key

def generatePublicKey():
    public_key = key.publickey().export_key()
    return public_key