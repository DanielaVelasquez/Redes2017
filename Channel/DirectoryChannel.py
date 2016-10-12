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
    def __init__ (self,receiver,directory_ip = None, my_port = DEFAULT_PORT, directory_port = None, username = None):
        super(DirectoryChannel,self).__init__(receiver, directory_ip,  directory_port ,my_port)
        self.username = username
        self.my_port = my_port
        self.my_ip = get_ip_address()

    #**************************************************
    #Metodo que se encarga de obtener lista de contactos
    #**************************************************
    def get_contacts(self):
        message = get_message('get_contacts_wrapper',[self.username])
        self.get_api_client().getProxy().send(message)
        data = self.get_api_client().getProxy().recv(BUFFER_SIZE_C)


    #**************************************************
    #Metodo que se encarga de  conectar al contacto
    #**************************************************
    def connect(self):
        message = get_message('connect_wrapper',[str(self.my_ip), str(self.my_port), str(self.username)])
        self.get_api_client().getProxy().send(message)
    
    #**************************************************#
    #Metodo que se encarga de  conectar al contacto    #
    #**************************************************#
    def disconnect(self):
        message = get_message('disconnect_wrapper',[self.username])
        self.get_api_client().getProxy().send(message)
        self.get_api_client().getProxy().close()

    def register_user(self,username,password):
        message = get_message('register',[username,password])
        self.get_api_client().getProxy().send(message)

    def login(self,username,password):
        print "Login"
        message = get_message('login',[username,password,str(self.my_ip), str(self.my_port)])
        self.get_api_client().getProxy().send(message)
        


