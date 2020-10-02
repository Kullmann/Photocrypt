import json
from http.server import BaseHTTPRequestHandler, HTTPServer


def make_handler(myvariable):

    class GetHandler(BaseHTTPRequestHandler):
        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

        def do_POST(self):
            self._set_headers()
            self.wfile.write(myvariable.encode('utf8'))
            return

        def do_SEAN(self):
            print("Hello World")
            return

    return GetHandler

server = HTTPServer(("localhost", 8080), make_handler('my_str'))
print ('Starting server, use <Ctrl-C> to stop')
server.serve_forever()