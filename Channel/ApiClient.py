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
from Constants import CHAT_PORT
from AuxiliarFunctions import *

"""**************************************************
Clase que genera un proxy para poder hacer uso de
los procedimientos remotos que ofrece la api del contacto
**************************************************"""
class MyApiClient:
    def __init__(self, contact_ip = None, contact_port = None):
        if contact_port:
            #TODO
        elif contact_ip:
            #TODO
        else:
            raise ValueError('The values of fields are not consistent MyApiClient.__init__')
