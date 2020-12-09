'''
author: Hosung Lee, Sean Kullmann
date: December 7 2020
Main program
'''

import sys
import argparse
from os.path import splitext, join, isfile
from photocrypt import open_image, encrypt_image, decrypt_image
from photocrypt.crypto.RSA import load_key, generate_key, save_keypair
from gui import startgui

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Encrypts or decrypts images using photocrypt package.'
        )

    parser.add_argument(
        '-i',
        metavar='image path',
        help='image file path to encrypt/decrypt'
        )

    parser.add_argument(
        '-k',
        metavar='key path',
        help='public key path'
        )

    parser.add_argument(
        '--encrypt',
        action='store_const',
        const=True,
        help='encrypt given image using provided key'
        )

    parser.add_argument(
        '--decrypt',
        action='store_const',
        const=True,
        help='decrypt given image using provided key'
        )
    
    parser.add_argument(
        '--genkey',
        action='store_const',
        const=True,
        help='generates rsa key to directory specified in -k'
        )

    use_cui = False
    encryption = None

    args = parser.parse_args()

    if args.genkey:
        path = args.k if args.k else '.'
        pub_path = join(path, 'public.pem')
        pri_path = join(path, 'private.pem')
        if isfile(pub_path) or isfile(pri_path):
            if isfile(pub_path):
                print(f"public key already exists at {pub_path}")
            if isfile(pri_path):
                print(f"private key already exists at {pri_path}")
            ans = input(f"do you want to overwrite? (Y/n) ")
            if ans not in ['Y', 'y', 'yes']:
                print("operation canceled.")
                sys.exit()
        save_keypair(generate_key(), (pri_path, pub_path))
        print(f'keys generated at {pub_path} {pri_path}')
        sys.exit()

    if args.encrypt and args.decrypt:
        print('can only perform encryption or decryption at once.')
        sys.exit()

    if args.encrypt or args.decrypt:
        if not args.i:
            print('image is required for encryption/decryption.')
            sys.exit()
        if not args.k:
            print('key is required for encryption/decryption.')
            sys.exit()

    if args.i and args.k:
        if not args.encrypt and not args.decrypt:
            print('use --encryption or --decryption to specify which to perform.')

        else:
            use_cui = True
            encryption = 'encrypt' if args.encrypt else 'decrypt'
    
    if use_cui:
        image = open_image(args.i)
        image_path, image_ext = splitext(args.i)
        key = load_key(args.k)
        if encryption == 'encrypt':
            encrypted = encrypt_image(image, key)
            encrypted.save(f'{image_path}_enc{image_ext}')
            print(f'image encrypted in {image_path}_enc{image_ext}')
        else:
            decrypted = decrypt_image(image, key)
            decrypted.save(f'{image_path}_dec{image_ext}')
            print(f'image decrypted in {image_path}_dec{image_ext}')
    else:
        # gui
        startgui()
