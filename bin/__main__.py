'''
@author: Hosung Lee, Sean Kullmann
@date: December 7 2020
@description: Main program
'''

import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Encrypts or decrypts images using photocrypt package.'
        )

    parser.add_argument(
        '-e',
        metavar='test image path',
        help='testing image on given path'
        )

    parser.add_argument(
        '-d',
        metavar='model path',
        help='set classifier model specified on given path'
        )

    args = parser.parse_args()
