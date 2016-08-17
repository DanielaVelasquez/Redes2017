#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *

class MyApiServer:
    def __init__(self,wrapper, my_port = DEFAULT_PORT):
        self.port = my_port
        self.server = SimpleXMLRPCServer((LOCALHOST,self.port),allow_none=True)
        print ("Conectando con "+LOCALHOST+" "+str(self.port))
        self.wrapper = wrapper
        self.server.register_instance(self.wrapper)
        print("Running")
        self.server.serve_forever()

        
class FunctionWrapper:
    def __init__(self):
        self.message = None

    """
    Procedimiento que ofrece nuestro servidor, este metodo sera llamado
    por el cliente con el que estamos hablando, debe de
    hacer lo necesario para mostrar el texto en nuestra pantalla.
    """
    def sendMessage_wrapper(self, message):
        self.message = message
        #print ("Mensaje "+self.message)
        self.showMessage()
    def showMessage(self):
        print ("Mensaje "+self.message)
        #raise  NotImplementedError( "Should have implemented this" )


a = FunctionWrapper()
b = MyApiServer(a)
