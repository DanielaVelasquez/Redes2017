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

        TCP_IP = contact_ip
        TCP_PORT = int(contact_port)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((TCP_IP, TCP_PORT))
        
        
    """**************************************************
    Metodos Get
    **************************************************"""
    def getProxy(self):
        return self.s