#! /usr/bin/env python
# -*- coding: utf-8 -*-


#####################################################
# PURPOSE: Clase que representa la abstracción de   #
#         Un canal bidireccional (con el servido de #
#         ubicacion), haciendo  uso de la biblioteca#
#         xmlRpc                                    #
#                                                   #
# Vilchis Dominguez Miguel Alonso                   #
#       <mvilchis@ciencias.unam.mx>                 #
#                                                   #
# Notes:                                            #
#                                                   #
# Copyright   16-08-2015                            #
#                                                   #
# Distributed under terms of the MIT license.       #
#####################################################
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *
from Constants.AuxiliarFunctions import *
from ApiServer import *
from Channels import *


class DirectoryChannel(BidirectionalChannel):
    def __init__ (self,receiver,directory_ip = None, my_port = None, directory_port = None, username = None):
        super(DirectoryChannel,self).__init__(receiver, directory_ip,  directory_port ,my_port)
        self.username = username
        self.my_port = my_port
        self.my_ip = get_ip_address()

    #**************************************************
    #Metodo que se encarga de obtener lista de contactos
    #**************************************************
    def get_contacts(self):
        self.get_api_client().getProxy().get_contacts_wrapper(username)


    #**************************************************
    #Metodo que se encarga de  conectar al contacto
    #**************************************************
    def connect(self):
        self.get_api_client().getProxy().connect_wrapper(str(self.my_ip), str(self.my_port), str(self.username))
    
    #**************************************************#
    #Metodo que se encarga de  conectar al contacto    #
    #**************************************************#
    def disconnect(self):
        elf.get_api_client().getProxy().disconnect_wrapper(self.username)
