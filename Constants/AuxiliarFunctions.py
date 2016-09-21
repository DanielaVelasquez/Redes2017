#! /usr/bin/env python
# -*- coding: utf-8 -*-


#####################################################
# PURPOSE:Funciones auxiliares                      #
#                                                   #
# Vilchis Dominguez Miguel Alonso                   #
#       <mvilchis@ciencias.unam.mx>                 #
#                                                   #
#                                                   #
# Copyright   16-08-2015                            #
#                                                   #
# Distributed under terms of the MIT license.       #
#####################################################
import socket


"""**************************************************
Metodo auxiliar que se conecta a internet para
conocer nuestra ip actual
**************************************************"""

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return "%s"% (s.getsockname()[0])




""" Funcion que construira el header del mensaje a mandar """
def get_message_header(username, ip):
    return username+':'+ip+':'


from Constants import *
def split_message_header(message):
    #El mensaje estara sera: username:ip:texto....
    message_split = message.split(':')
    return (message_split[MESSAGE_IP], message_split[MESSAGE_PORT], message_split[2:])


