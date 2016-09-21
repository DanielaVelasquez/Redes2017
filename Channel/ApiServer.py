#! /usr/bin/env python
# -*- coding: utf-8 -*-


#####################################################
# PURPOSE: Clase que permite mandar un mensaje al   #
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
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
#  Mis bibliotecas
import sys
from AuxiliarFunctions import *
from Constants import *

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
"""**************************************************
Clase que genera un servidor de la biblioteca xmlrpc
con el cual el cliente expondra los metodos que ofrece
**************************************************"""
class MyApiServer:
    def __init__(self,Qparent, my_port = DEFAULT_PORT):
        self.port = my_port
        self.server = SimpleXMLRPCServer((get_ip_address(),int(self.port)),allow_none=True)
        self.wrapper = FunctionWrapper()
        self.server.register_instance(self.wrapper)
        self.server.serve_forever()


class FunctionWrapper:
    """ **************************************************
    Constructor de la clase
    ************************************************** """
    def __init__(self):
        #Diccionario que contiene las conversaciones activas 
        #hasta ese momento
        self.chats_dictionary = {}
        

    """**************************************************
    Metodo que sera llamado cuando un contacto quiera establecer
    conexion con este cliente
    **************************************************"""
    def new_chat_wrapper(self, contact_ip, contact_port, username):
        #Un cliente mando a llamar a esta instancia, crea una ventana de
        #chat para automaticamente
        #TODO

    """ **************************************************
    Procedimiento que ofrece nuestro servidor, este metodo sera llamado
    por el cliente con el que estamos hablando, debe de
    hacer lo necesario para mostrar el texto en nuestra pantalla.
    ************************************************** """
    def sendMessage_wrapper(self, message):
        #Recuerden que el mensaje, al inicio debe llevar una cadena
        #que contiene username:ip,  para saber a que conversacion 
        #se refiere
        message_split = split_message_header(message)
        contact_ip =  message_split[MESSAGE_IP]
        contact_port = message_split[MESSAGE_PORT]
        text = message_split[MESSAGE_TEXT]
        
    """ **************************************************
    Procedimiento que ofrece nuestro servidor, este metodo sera llamado
    por el cliente con el que estamos hablando, debe de
    hacer lo necesario para regresar el texto
    ************************************************** """
    def echo(self, message):
        #TODO
    """ **************************************************
    Procedimiento que ofrece nuestro servidor, este metodo sera llamado
    por el cliente con el que estamos hablando, debe de
    hacer lo necesario para reproducir el audio
    ************************************************** """
    def play_audio_wrapper(self,audio):
        #TODO
     
    """ **************************************************
    Procedimiento que ofrece nuestro servidor, este metodo sera llamado
    por el cliente con el que estamos hablando, debe de
    hacer lo necesario para reproducir el video en la ventana adecuada
    ************************************************** """
    def play_video_wrapper(self,frame):
        #TODO
    
