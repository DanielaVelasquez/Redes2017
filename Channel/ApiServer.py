#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *
from RecordAudio import AudioServer
import threading
"""
Clase MyApiClient que servira como el servidor de cada instancia del programa
"""
class MyApiServer:
    """
    Constructor de la clase
    @param <FunctionWrapper> wrapper: objeto que recibe los mensajes del cliente
    @param <int> my_port: especifica el puerto donde se debe hacer la conexion
    """
    def __init__(self,wrapper, my_port = DEFAULT_PORT):
        self.port = my_port
        try:
            self.server = SimpleXMLRPCServer((LOCALHOST,int(self.port)),allow_none=True)
        except Exception:
            raise Exception(PORT_IN_USE)
        self.wrapper = wrapper
        self.audioServer = AudioServer()
        self.server.register_function(self.audioServer.playAudio, 'playAudio') 
        self.server.register_instance(self.wrapper)
        self.server.serve_forever()

"""
Clase Function wrapper para la ejecucion de metodos remotos
"""
class FunctionWrapper(object):
    """
    Constructor
    """
    def __init__(self):
        self.message = None

    """
    Procedimiento que ofrece nuestro servidor, este metodo sera llamado
    por el cliente con el que estamos hablando, debe de
    hacer lo necesario para mostrar el texto en nuestra pantalla.
    """
    def sendMessage_wrapper(self, message):
        self.message = message

    


