#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *

class MyApiClient:
    def __init__(self, contact_port = DEFAULT_PORT,contact_ip=LOCALHOST_CLIENT):
    	self.contact_port = contact_port
    	self.contact_ip = contact_ip
    	self.proxy = xmlrpclib.ServerProxy(contact_ip+str(self.contact_port)+"/", allow_none=True)
    	print ("Conectando con "+contact_ip+str(self.contact_port)+"/")
    
    def sendMessage(self,message):
    	print "enviando"
    	#self.proxy = xmlrpclib.ServerProxy(contact_ip+str(self.contact_port)+"/")
    	self.proxy.sendMessage_wrapper(message)

a = MyApiClient()
a.sendMessage("Hola")
#a.sendMessage("Funciono maldita sea")