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
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.AuxiliarFunctions import *
from Constants.Constants import *

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)
"""**************************************************
Clase que genera un servidor de la biblioteca xmlrpc
con el cual el cliente expondra los metodos que ofrece
**************************************************"""
class MyApiServer:
	def __init__(self,app_receiver,my_port = DEFAULT_PORT,):
		#self,Qparent, my_port = DEFAULT_PORT
		self.port = my_port
		self.server = SimpleXMLRPCServer((get_ip_address(),int(self.port)),allow_none=True)
		self.wrapper = FunctionWrapper(app_receiver)
		self.server.register_instance(self.wrapper)
	  
	"""**************************************************
	Inicia el servidor para que atienda peticiones
	**************************************************"""  
	def startServer(self):
		self.server.serve_forever()


class FunctionWrapper():
	""" **************************************************
	Constructor de la clase
	************************************************** """
	def __init__(self,receiver):
		#Diccionario que contiene las conversaciones activas 
		#hasta ese momento
		self.receiver = receiver
		self.chats_dictionary = {}
	  
	def searchUser(self,ip,port):
		for user in self.chats_dictionary:
			if user[IP_CONTACT] == ip and user[PORT_CONTACT] == port:
				return user
		return None


	"""**************************************************
	Metodo que sera llamado cuando un contacto quiera establecer
	conexion con este cliente
	**************************************************"""
	def new_chat_wrapper(self, contact_ip, contact_port, username):
		user = dictionaryUser(username,contact_ip,contact_port)
		self.chats_dictionary[username] = user
		self.receiver.showNewChat(contact_ip, contact_port, username)
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
		user = searchUser(contact_ip,contact_port)
		self.receiver.showMessage(user,text)
		
	""" **************************************************
	Procedimiento que ofrece nuestro servidor, este metodo sera llamado
	por el cliente con el que estamos hablando, debe de
	hacer lo necesario para regresar el texto
	************************************************** """
	def echo(self, message):
		pass
		#TODO
	
	def play_audio_wrapper(self,audio):
		pass
		#TODO
	 
	""" **************************************************
	Procedimiento que ofrece nuestro servidor, este metodo sera llamado
	por el cliente con el que estamos hablando, debe de
	hacer lo necesario para reproducir el video en la ventana adecuada
	************************************************** """
	def play_video_wrapper(self,frame):
		pass
		#TODO
	


#***************************************************************************************************************
"""""
Clase encargada de recibir las notificaciones del servidor,
se trabajará como si fuera una interface, así quien reciba 
las notificaciones del servidor podrá ser implementado como 
sea mejor, sólo deberá heredar de receiver y puede ser una GUI
o otro medio de interacción con el usuario
"""
class Receiver(object):
	 """User: usuario al cual está asociado el recibidor, define para qué usuario trabaja"""
	 def __init__(self,user):
		 super(Receiver, self).__init__()
		 self.user = user
	


	 def showNewChat(self, contact_ip, contact_port, username):
		 raise NotImplementedError()

	 def showMessage(self, user,message):
		 raise NotImplementedError()
		
	
	 def play_audio(self,audio):
		 raise NotImplementedError()
	 
	 def play_video_wrapper(self,frame):
		 raise NotImplementedError()