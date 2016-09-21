#! /usr/bin/env python
# -*- coding: utf-8 -*-


#####################################################
# PURPOSE: Clase que permite hacer uso de la api del#
#           contacto                                #
#                                                   #
# Vilchis Dominguez Miguel Alonso                   #
#       <mvilchis@ciencias.unam.mx>                 #
#                                                   #
# Notes:                                            #
#                                                   #
# Copyright   17-08-2015                            #
#                                                   #
# Distributed under terms of the MIT license.       #
#####################################################
import xmlrpclib
import sys
sys.path.insert(0, '../Constants')
from Constants import *
from AuxiliarFunctions import *


"""**************************************************
Clase que genera un proxy para poder hacer uso de
los procedimientos remotos que ofrece la api del contacto
**************************************************"""
class MyApiClient:
    def __init__(self, contact_ip = None, contact_port = None):
        if contact_port is None:
            contact_port = DEFAULT_PORT
        elif contact_ip is None:
            contact_ip = LOCALHOST_CLIENT
        self.contact_port = contact_port
        self.contact_ip = contact_ip
        try:
        	self.proxy = xmlrpclib.ServerProxy(HTTP+str(self.contact_ip)+":"+str(self.contact_port)+"/", allow_none=True)
        except Exception, e:
        	raise Exception(CONECTION_FAIL)
        
    """**************************************************
    Metodos Get
    **************************************************"""
    def getProxy(self):
    	return self.proxy