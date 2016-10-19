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
import socket,select
import ast,time
#  Mis bibliotecas
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.AuxiliarFunctions import *
from Constants.Constants import *
from RecordAudio import AudioServer
from RecordVideo import VideoServer

import threading
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, QObject

import struct
import pickle

"""**************************************************
Clase que genera un servidor de la biblioteca xmlrpc
con el cual el cliente expondra los metodos que ofrece
**************************************************"""
class MyApiServer:
	def __init__(self,app_receiver,my_port = DEFAULT_PORT):
		try:
			self.wrapper = FunctionWrapper(app_receiver)
			TCP_IP = get_ip_address()
			TCP_PORT = int(my_port)
			#Inicia el servidor
			self.port = my_port
			self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			#Conexiones actuales
			self.users = {}
			self.s.bind((TCP_IP, TCP_PORT))
			self.s.listen(500)
			self.running = False
			print ("Server at (%s, %s))"%(TCP_IP, TCP_PORT))
		except Exception as e:
			raise Exception("API SERVER "+PORT_IN_USE+"\n"+str(e))		
		
	def startServer(self):
		self.running = True
		while self.running:
			conn, addr = self.s.accept()
			threading.Thread(target = self.run_thread, args = (conn,addr)).start()
		self.s.close()

	def stop_server(self):
		self.running = False
	
	def run_thread(self, conn, addr):
		print "Client connected with "+addr[0]+ ":"+str(addr[1])
		connected = True
		payload_size = struct.calcsize("L")
		data = ""
		while connected:
			try:
				chunk = conn.recv(BUFFER_SIZE_C)

				if not chunk:
					break
				
				if is_audio(chunk):
					self.wrapper.play_audio_wrapper(chunk)
					#time.sleep(3)

				else:
					# Frame de video recibido
					if len(data) >= payload_size:
						packed_msg_size = data[:payload_size]
						data = data[payload_size:]
						msg_size = struct.unpack("L", packed_msg_size)[0]
						while len(data) < msg_size:
							data += conn.recv[BUFFER_SIZE_VIDEO]
						frame_data = data[:msg_size]
						data = data[msg_size:]
						frame = pickle.loads(frame_data)
						self.wrapper.play_video_wrapper(frame)
						
					if FINAL in chunk:
						val = chunk
						data += val.replace(FINAL,"")
						chunk = FINAL

					if chunk  == FINAL:
						#print "Data recived: "+data
						method, params = get_method(data)
						if method == 'new_chat_wrapper':
							self.wrapper.new_chat_wrapper(params[0],params[1],params[2])
						elif method == 'add_contact':
							self.wrapper.add_contact(params[0],params[1],params[2])
						elif method == 'audio_state':
							self.wrapper.audio_state(params[0],params[1])
						elif method == 'remove_contact':
							self.wrapper.remove_contact(params[0])
						elif method == 'sendMessage_wrapper':
							self.wrapper.sendMessage_wrapper(params[0])
						elif method == 'play_audio_wrapper':
							#print "Data server: "+data
							self.wrapper.play_audio_wrapper(params[0])
						elif method == 'update_contacts':
							contacts = ast.literal_eval(params[0])
							self.wrapper.update_contacts(contacts)
						else:
							print "Not registered method "+str(data)
						data = ""

					else:
						data += chunk


			except Exception as e:
				connected = False
		conn.close()

	def get_wrapper(self):
		return self.wrapper

class FunctionWrapper(QtCore.QThread):
	""" **************************************************
	Constructor de la clase
	************************************************** """
	def __init__(self,receiver):
		QtCore.QThread.__init__(self)
		#Diccionario que contiene las conversaciones activas 
		#hasta ese momento
		self.chats_dictionary = {}
		self.receiver = receiver
		self.audio_server = AudioServer()
		self.video_server = VideoServer()	
	  
	def search_user(self,ip,port):
		for c in self.chats_dictionary:
			user = self.chats_dictionary[c]
			if user[IP_CONTACT] == ip and user[PORT_CONTACT] == port:
				return user
		return None

	#Le indica a un usuario cuando se genera un evento de envio voz
	def audio_state(self,username,state):
		self.receiver.state_audio(username,state)

	"""**************************************************
	Metodo que sera llamado cuando un contacto quiera establecer
	conexion con este cliente
	**************************************************"""
	def new_chat_wrapper(self, contact_ip, contact_port, username):
		user = dictionaryUser(username,contact_ip,contact_port)
		self.chats_dictionary[username] = user
		self.receiver.showNewChat(contact_ip, contact_port, username)
		#Emite la señal para que se cree la ventana		
		self.emit(SIGNAL(SIGNAL_CREATE_WINDOW))
		#Un cliente mando a llamar a esta instancia, crea una ventana de
		#chat automaticamente

	def add_contact(self,contact_ip,contact_port,username):
		user = dictionaryUser(username,contact_ip,contact_port)
		self.chats_dictionary[username] = user

	###################################################
	#Método que es llamado por un contacto cuando     #
	#quiere indicar que no se van a comunicar más     #
	###################################################
	def remove_contact(self, username):		
		if self.chats_dictionary.has_key(username):
			del self.chats_dictionary[username]
			self.receiver.remove_contact(username)		

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
		text = message_split[MESSAGE_TEXT]
		user = message_split[MESSAGE_USER]
		self.receiver.showMessage(user,text)		
		
	""" **************************************************
	Procedimiento que ofrece nuestro servidor, este metodo sera llamado
	por el cliente con el que estamos hablando, debe de
	hacer lo necesario para regresar el texto
	************************************************** """
	def echo(self, message):
		pass
	
	def play_audio_wrapper(self,audio):
		self.audio_server.playAudio(audio)		
	 
	""" **************************************************
	Procedimiento que ofrece nuestro servidor, este metodo sera llamado
	por el cliente con el que estamos hablando, debe de
	hacer lo necesario para reproducir el video en la ventana adecuada
	************************************************** """
	def play_video_wrapper(self,frame):
		self.video_server.reproduce(frame)		

	def update_contacts(self,contact):
		self.receiver.show_contacts(contact)

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

	 #Abre la ventana al recibir la señal
	 def open_window(self):
		raise NotImplementedError()

	 def remove_contact(self,username):
		raise NotImplementedError()

	 ####################################################
	 #Indica se cerró la conexión con el usuario con    #
	 #nombre de usuario 'username'                      #
	 ####################################################
	 def close_connection_with(self, username):
		raise NotImplementedError()

	 def state_audio(self,username,state):
		raise NotImplementedError()

	 def show_contacts(self,contacts):
		raise NotImplementedError()
