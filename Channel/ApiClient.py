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
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *
from Constants.AuxiliarFunctions import *


"""**************************************************
Clase que genera un proxy para poder hacer uso de
los procedimientos remotos que ofrece la api del contacto
**************************************************"""
class MyApiClient:
    def __init__(self, contact_ip = None, contact_port = None):
        if contact_port is None:
            contact_port = DEFAULT_PORT
        elif contact_ip is None:
            contact_ip = get_ip_address()

        self.contact_port = contact_port
        self.contact_ip = contact_ip
        try:
            con = HTTP+str(self.contact_ip)+":"+str(self.contact_port)+"/"
            print "Client coneccting to: "+con
            self.proxy = xmlrpclib.ServerProxy(con, allow_none=True)
            print "I'm client, server has this methods: "+str(self.proxy.system.listMethods())
        except Exception, e:
        	raise Exception(CONECTION_FAIL)
        
    """**************************************************
    Metodos Get
    **************************************************"""
    def getProxy(self):
        try:
            con = HTTP+str(self.contact_ip)+":"+str(self.contact_port)+"/"
            self.proxy = xmlrpclib.ServerProxy(con, allow_none=True)
        except Exception, e:
            raise Exception(CONECTION_FAIL)
    	return self.proxy