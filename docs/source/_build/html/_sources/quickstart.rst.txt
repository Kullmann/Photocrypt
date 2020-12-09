Quick Start
===========

This page will show simple usages of our package.

Generate Keys
-------------

The code below shows how to generate keys::

    from photocrypt.crypto.RSA import generate_key, save_keypair
    
    # generate key pair
    private_key, public_key = generate_key()

    # save key pair
    save_keypair((private_key, public_key), ("private.pem", "public.pem"))

Encrypt Image
-------------

The code below shows how to load public key and encrypt an image::

    from photocrypt import open_image, encrypt_image
    from photocrypt.crypto.RSA import load_key

    # open image
    image = open_image("samples/tuatara.jpg")

    # load public key
    public_key = load_key("public.pem")

    # encrypt image
    image_enc = encrypt_image(image, public_key)

    # save image
    image.save("samples/tuatara_enc.jpg")

Decrypt Image
-------------

The code below shows how to load private key and decrypt an image::

    from photocrypt import open_image, decrypt_image
    from photocrypt.crypto.RSA import load_key

    # open image
    image = open_image("samples/tuatara_enc.jpg")

    # load private key
    private_key = load_key("private.pem")

    # encrypt image
    image_enc = encrypt_image(image, private_key)

    # save image
    image.save("samples/tuatara_dec.jpg")