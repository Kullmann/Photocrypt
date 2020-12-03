def loadPublicKey(imgdata):
    #imgdata = imgdata[:-1]
    with open("../../keys/receiver.pem", "wb") as f:
        f.write(imgdata)


def loadPrivateKey(imgdata):
    #imgdata = imgdata[:-1]
    with open("../../keys/private.pem", "wb") as f:
        f.write(imgdata)
