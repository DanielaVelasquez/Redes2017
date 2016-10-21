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
import socket
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

        self.contact_port = int(contact_port)
        self.contact_ip = contact_ip
        TCP_IP = contact_ip
        TCP_PORT = int(contact_port)

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
            self.s.connect((TCP_IP, TCP_PORT))
            #print "Client connecting with "+str((TCP_IP, TCP_PORT))
        except Exception as e:
            raise Exception("API CLIENT "+PORT_IN_USE)
        
        
        
        
    """**************************************************
    Metodos Get
    **************************************************"""
    def getProxy(self):
        return self.s

    def get_address(self):
        return (self.contact_ip,self.contact_port)