from http.server import BaseHTTPRequestHandler,HTTPServer, SimpleHTTPRequestHandler
import ssl
import logging
import json

def encryt(raw_photo):
    return None

class GetHandler(SimpleHTTPRequestHandler):

        def do_GET(self):
            logging.error(self.headers)
            SimpleHTTPRequestHandler.do_GET(self)

        def do_POST(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            d = self.data_string.decode("utf-8").split("message=")[1:]
            print(d)
            data = b'<html><body><h1>POST!</h1></body></html>'
            self.wfile.write(bytes(data))
            return

Handler=GetHandler

logging.basicConfig(level=logging.DEBUG)
httpd=HTTPServer(("localhost", 8080), Handler)
#httpd.socket =ssl.wrap_socket(httpd.socket, certfile='/tftpboot/server.pem', server_side=True)
httpd.serve_forever()