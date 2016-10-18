#! /usr/bin/env python
# -*- coding: utf-8 -*-


#####################################################
# PURPO: Clase que representa la abstracción de   #
#         Un canal bidireccional, con uso de la     #
#          biblioteca xmlRpc                        #
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

from ApiServer import *
from ApiClient import *
from RecordAudio import AudioClient
import xmlrpclib
import multiprocessing as mp
import threading
import numpy

import sys,getopt
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Constants.Constants import *
#from RecordAudio import record_audio_queue
"""**************************************************
Las instancias de esta clase contendran los metodos
necesarios para hacer uso de los metodos
del api de un contacto. Internamente Trabajara
con una proxy apuntando hacia los servicios del
servidor xmlrpc del contacto
**************************************************"""
class RequestChannel(object):
    """**************************************************
    Convencion: Si trabajamos de manera local, entonces
    haremos uso de los campos de contact_port y my_port
    por lo que el campo de contact_ip puede ser nulo.
    Si trabajamos con instancias en la red solo se hara uso
    del campo de contact_ip
    **************************************************"""
    """**************************************************
    Constructor de la clase
    @param <str> contact_ip: Si no se trabaja de manera local
                representa la ip del contacto con el que se
                establecera la conexion
    @param <int> my_port: De trabajar de manera local puerto
                de la instancia del cliente
    @param <int> contact_port: De trabajar de manera local
                representa el puerto de la instancia del contacto
    **************************************************"""
    def __init__(self, contact_ip = None, contact_port = None, sender = None):
        super(RequestChannel,self).__init__()
        if sender:
            self.api_client = MyApiClient(contact_port= contact_port,contact_ip= contact_ip) 
        else:
            #Crea el cliente
            if contact_port:
                self.api_client = MyApiClient(contact_port= contact_port) 
            elif contact_ip:
                self.api_client = MyApiClient(contact_ip= contact_ip)
            else:
                raise Exception("Request channel "+ERROR_REQUEST_CHANNEL)

        self.calling = False

    """**************************************************
    Metodo que se encarga de mandar texto al contacto con
    el cual se estableció la conexion
    **************************************************"""
    def send_text(self, text):
        print "I'm request channel, sending: "+text
        message = get_message('sendMessage_wrapper',[text])
        send_message_chunks(self.api_client.getProxy(),message)
        #self.api_client.getProxy().send(message)


    
    """**************************************************
    Metodo que se encarga de mandar iniciar una conversacion
    con un nuevo contacto 
    **************************************************"""
    def new_connection(self, my_ip, my_port,my_username):
        message = get_message('new_chat_wrapper',[my_ip,my_port,my_username])
        send_message_chunks(self.api_client.getProxy(),message)
        #self.api_client.getProxy().send(message)   
    
    def remove_connection_with(self,username):
        message = get_message('remove_contact',[username])
        send_message_chunks(self.api_client.getProxy(),message)
        #self.api_client.getProxy().send(message)   


    def send_audio(self):
        self.audioRecorder = AudioClient(self.api_client.getProxy())
        self.call_thread = threading.Thread(target=self.audioRecorder.record)
        self.call_thread.daemon = True
        self.call_thread.start()

    def stops_sending_audio(self):
        self.audioRecorder.stream.stop_stream()

    def audio_state(self,username, state):
        message = get_message('audio_state',[username,state])
        send_message_chunks(self.api_client.getProxy(),message)
        #self.api_client.getProxy().send(message)

    def send_contacts(self,contacts):

        """
        conts = ""
        for c in contacts:
            conts = conts + SEP_LIST
        print "conts: "+str(conts)
        """
        print "Channel sending contacts"+str(contacts)

        message = get_message('update_contacts',[contacts])
        send_message_chunks(self.api_client.getProxy(),message)
        #self.api_client.getProxy().send(message)

    """**************************************************
    Metodo que se encarga de mandar audio y video al contacto 
    con el cual se estableció la conexion
    **************************************************"""
    #def begin_call(self):
        #TODO

    """**************************************************
    Metodos Get
    **************************************************"""
    def get_api_client(self):
        return self.api_client

    


#***************************************************************************************************************
import threading
class BidirectionalChannel(RequestChannel):
    def __init__(self, receiver, contact_ip = None,  contact_port = None,my_port = None):
        super(BidirectionalChannel,self).__init__(contact_ip = contact_ip, contact_port = contact_port)
        
        #Conexión local
        if my_port and contact_port:
            #El objeto api server necesita correr en un hilo aparte
            #Crea el servidor
            self.apiServer = MyApiServer(receiver,my_port)
        elif contact_ip:
            self.apiServer = MyApiServer(receiver)
        else:
            raise ValueError('The values of fields are not consistent BidirectionalChannel.__init__')
        
        #Lanza el servidor
        self.server_thread = threading.Thread(target = self.apiServer.startServer) 
        self.server_thread.daemon = True
        self.server_thread.start()

    def get_server(self):
        return self.apiServer
    """**************************************************
    Metodos Get
    **************************************************"""
    """"def get_api_server(self):
        return self.api_server_thread
    """
