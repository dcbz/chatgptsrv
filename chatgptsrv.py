#!/usr/bin/env python

from chatgpt import Conversation
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json

GPTSRVPORT = 4321

class S(BaseHTTPRequestHandler):
    def get_chat(self,msg):
        conversation = Conversation(timeout=3000)
        answer = conversation.chat(msg)
        conversation.reset()
        return answer

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 
        self._set_response()
        try:
            msg = json.loads(post_data) # should probably fail more gracefully
        except:
            self.wfile.write(json.dumps("An error occured."))
            return
        json.dumps(self.wfile.write(self.get_chat(msg).encode('utf-8')))
            

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('127.0.0.1', port) # local only
    httpd = server_class(server_address, handler_class)
    logging.info('Starting ChatGPTSrv\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping ChatGPTSrv...\n')

if __name__ == '__main__':
    from sys import argv

    run(port=GPTSRVPORT)