#! /usr/bin/env python
# -*- coding: utf-8 -*-

import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *
from Constants.AuxiliarFunctions import *

from ApiClient import MyApiClient
from ApiServer import MyApiServer
from ApiServer import FunctionWrapper

import threading
import time
"""
Las instancias de esta clase contendran los metodos
necesarios para hacer uso de los metodos
del api de un contacto. Internamente Trabajara
con una proxy apuntando hacia los servicios del
servidor xmlrpc del contacto
"""
class Channel:
    """
    Constructor de la clase
    @param <str> contact_ip: Si no se trabaja de manera local
                representa la ip del contacto con el que se
                establecera la conexion
    @param <int> my_port: De trabajar de manera local puerto
                de la instancia del cliente
    @param <int> contact_port: De trabajar de manera local
                representa el puerto de la instancia del contacto
    """
    def __init__(self, contact_ip = None, my_port = None,contact_port = None):
        self.contact_ip = contact_ip
        self.contact_port = contact_port
        self.my_port  = my_port
        self.server_connection_done = False
        self.client_connection_done = False
        self.server = None
        self.client = None
        self.wrapper = None

    """""
    Inicia los hilos del chat, primero inicia el servidor
    y despues inicia los hilos del cliente
    """
    def init_chat(self):
        self.server_thread = threading.Thread(target=self.init_server)
        self.client_thread = threading.Thread(target=self.init_client)
        #Inicio de los hilos
        self.server_thread.start()
        self.client_thread.start()


    """"
    Asigna un nuevo wrapper al wrapper de la clase
    """
    def setWrapper(self,wrapper):
        self.wrapper = wrapper

    """"
    Metodo que se encarga de mandar texto al contacto con
    el cual se estableció la conexion, retorna verdadero
    si el mensaje se envio efectivamente
    """
    def send_text(self, text):
        #mutex_server.acquire()
        #mutex_client.acquire()
        
        print "channel: "+text
        if self.client is not None:
            answer = self.client.sendMessage(text)
            #mutex_client.release()
            #mutex_server.release()
            return answer
        #mutex_client.release()
        #mutex_server.release()
        return False

    """"
    Inicia el servidor considerando que se tengan
    los valores necesarios para iniciarlo
    """
    def init_server(self):
        if self.wrapper is None:
            raise Exception(MISSING_WRAPPER)
        elif self.my_port is None:
            #mutex_server.acquire()
            self.server = MyApiServer(self.wrapper)
        else:
            #mutex_server.acquire()
            self.server = MyApiServer(self.wrapper,self.my_port)

    """""
    Inicia el cliente
    """
    def init_client(self):
        #mutex_client.acquire()
        self.client = MyApiClient(self.contact_port,self.contact_ip)
        #mutex_server.release()


