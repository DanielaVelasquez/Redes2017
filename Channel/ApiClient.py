#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *

class MyApiClient:
	
    def __init__(self, contact_port,contact_ip):
    	if contact_port is None:
    		contact_port = DEFAULT_PORT
    	if contact_ip is None:
    		contact_ip = LOCALHOST_CLIENT
    	self.contact_port = contact_port
    	self.contact_ip = contact_ip
    	self.proxy = xmlrpclib.ServerProxy(contact_ip+str(self.contact_port)+"/", allow_none=True)
    	"""
	    Constructor de la clase
	    @param <int> contact_port: especifica el puerto de contacto del contacto, 
	    			 en caso de no especificarse se toma el puerto por defecto
	    @param <str> contact_ip: especifica la ip del contacto en caso de no 
	    			 trabajar de forma local, si no se especfica toma por defecto
	    			 localhost
	    """
    
    """"
    Envia el mensaje al servidor que se encuentra conectado
    @param <str> message: mensaje que se desea enviar
    """
    def sendMessage(self,message):
    	print("Estoy en el cliente voy a enviar "+message)
    	self.proxy.sendMessage_wrapper(message)

