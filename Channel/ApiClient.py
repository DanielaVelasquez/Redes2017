#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *
"""
Clase MyApiClient que servira como el cliente de cada instancia del programa
"""
class MyApiClient:
    """
    Constructor de la clase
    @param <int> contact_port: especifica el puerto de contacto del contacto, 
    en caso de no especificarse se toma el puerto por defecto
    @param <str> contact_ip: especifica la ip del contacto en caso de no 
    trabajar de forma local, si no se especfica toma por defecto localhost
    """
    def __init__(self, contact_port,contact_ip):
        print "contact ip: "+str(contact_ip)
        if contact_port is None:
            contact_port = DEFAULT_PORT
        if contact_ip is None:
            contact_ip = LOCALHOST_CLIENT
        self.contact_port = contact_port
        self.contact_ip = contact_ip
           
    """"
    Envia el mensaje al servidor que se encuentra conectado
    @param <str> message: mensaje que se desea enviar
    """
    def sendMessage(self,message):
        print "-) Api client: "+message
        try:
            print "cliente: "+str(self.contact_ip)+str(self.contact_port)+"/"
            self.proxy = xmlrpclib.ServerProxy(self.contact_ip+str(self.contact_port)+"/", allow_none=True)
            self.proxy.sendMessage_wrapper(str(message))
            return True
        except Exception, ex:
            return False