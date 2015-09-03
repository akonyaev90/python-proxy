#!/usr/bin/python

__author__ = 'akonyaev'

import asyncore
import socket
import json

key_buffer = {}

json_config=open('./config.json').read()
config= json.loads(json_config)
modify_module = __import__(config['modify_script'])

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        global key_buffer
        res = ''
        data = self.recv(config['buffer_size'])
        if data:
            modify_module.modify_function(data,self,key_buffer)
            server_remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_remote.connect ((config['output']['address'], config['output']['port']))
            server_remote.send(res)
            server_remote.close()

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(config['max_connections'])

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            handler = EchoHandler(sock)

server = EchoServer(config['input']['address'], config['input']['port'])
asyncore.loop()