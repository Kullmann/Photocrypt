#!/usr/bin/env python
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler,HTTPServer, SimpleHTTPRequestHandler
from encrypt import *
from decrypt import *
from generateKeys import *
import ssl
import logging
import json
import base64
import io
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg

serv_name = "localhost"
#serv_name = "192.168.1.19"
serv_port = 8080

class PhotoCryptoHandler(SimpleHTTPRequestHandler):
        # post method
        def do_POST(self):

            # header
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # get raw data
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            
            # convert raw data to base64 data
            base64_encoded_data = self.data_string.decode("utf-8").split(',')[-1]

            # convert base64 data to image data
            imgdata = base64.b64decode(base64_encoded_data)
            #imgdata = (base64_encoded_data)


            # show received image
            # imgdata = io.BytesIO(imgdata)
            # imgdata = mpimg.imread(imgdata, format='PNG')
            # imgplot = plt.imshow(image)
            # plt.show()

            # result variable
            result = None

            # encrypt photo
            if self.path == "/encrypt":
                result = encrypt(imgdata)
                imgdata = base64.b64encode(result)
                with open('logging.txt', 'wb') as f:
                    f.write(imgdata)
                result = imgdata

            # decrypt photo
            elif self.path == "/decrypt":
                result = decrypt(imgdata)
                imgdata = base64.b64encode(result)
                result = imgdata

            elif self.path == "/generatePrivateKey":
                private_key = generatePrivateKey()
                result = private_key

            elif self.path == "/generatePublicKey":
                public_key = generatePublicKey()
                result = public_key

            # if result is empty, send "no output" to client
            if result == None:
                self.wfile.write(b'no output')
                return
            
            #print("result: ")
            #print(result)

            # print(f"recieved {imgdata}")
            self.wfile.write(bytes(result))
            return

# logging config
logging.basicConfig(level=logging.DEBUG)

# init server
httpd=HTTPServer((serv_name, serv_port), PhotoCryptoHandler)
# print start message
print(f"server started on {serv_name}:{serv_port}")

# start server
httpd.serve_forever()
