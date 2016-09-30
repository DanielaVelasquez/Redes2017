#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
#Direcciones relativas
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Channel.Channels import RequestChannel
from Constants.Constants import *
from Constants.AuxiliarFunctions import *
from Channel.ApiServer import Receiver

"""
Clase de interfaz grafica que permite visualizar la conversacion con el contacto del chat
Y enviar nuevos mensajes por medio de un campo de texto
"""
class ChatGUI(QtGui.QWidget):
	"""
	Constructor
	@param <str> my_user: información del usuario
    @param <str> my_contact: informacion del contacto para la conexion
    @param <str> mode: modo en el que operara el programa (constantes LOCAL o REMOTE)
	"""
	def __init__(self, my_user, my_contact, mode,my_parent_receiver):
		super(ChatGUI, self).__init__()
		self.my_parent_receiver = my_parent_receiver
		self.my_user = my_user
		self.my_contact = my_contact
		self.mode = mode


		try:
			#Canal de comunicación con el contacto
			self.request_channel = None
			self.create_request_channel()
			self.initGUI()
			self.connection_open = True
			self.my_parent_receiver.add_contact_receiver(self.my_contact)
		except Exception as e:
			QtGui.QMessageBox.warning(self, WARNING, str(e),QtGui.QMessageBox.Ok)
		
	#*******************************************#
	#Realiza la conexión con el contacto        #
	#*******************************************#
	def create_request_channel(self):
		if self.mode in LOCAL:
			self.request_channel = RequestChannel(contact_port = self.my_contact[PORT_CONTACT])
		else:
			self.request_channel = RequestChannel(contact_ip = self.my_contact[IP_CONTACT])

		
	#********************************************#
	#Manda a iniciar una nueva conversación      #
	#********************************************#
	def connect(self):
		self.request_channel.new_connection(self.my_user[IP_CONTACT], self.my_user[PORT_CONTACT],self.my_user[NAME_CONTACT])
	
	#******************************************************#
	#Inicia los elementos de la GUI, mostrando la ventana  #
	#donde se reciben los mensaje y una que permite enviar #
	#los mensajes                                          #
	#******************************************************#
	def initGUI(self):		
		#Creación y configuración del widget
		self.setWindowTitle(CHAT_WINDOW)
		self.setGeometry(DEFAULT_POSITION_X+10, DEFAULT_POSITION_Y+10, CHAT_WIDTH, CHAT_HEIGHT)
		self.resize(500,200)
		#Configuración layout
		self.grid = QtGui.QGridLayout()
		self.setLayout(self.grid)
		#Declaración elementos de la GUI
		self.lb_conversation = QtGui.QLabel(CONVERSATION_TITLE+" de "+self.my_user[NAME_CONTACT]+" ->"+self.my_contact[NAME_CONTACT],self)
		self.txt_conversation = QtGui.QTextEdit(self)
		self.txt_conversation.setReadOnly(True)
		self.txt_message = QtGui.QLineEdit(self)
		self.btn_send = QtGui.QPushButton(SEND_TITLE,self)
		self.btn_call = QtGui.QPushButton(CALL_TITLE,self)
		#Configuración elementos de la GUI 
		self.grid.addWidget(self.lb_conversation,0,0)
		self.grid.addWidget(self.txt_conversation,1,0,10,10)		
		self.grid.addWidget(self.txt_message,11,0,5,1)
		self.grid.addWidget(self.btn_send,12,4,3,2)
		self.btn_call.setStyleSheet("background-color: DodgerBlue")
		self.grid.addWidget(self.btn_call,15,4,3,2)

		self.btn_send.clicked.connect(self.send_message)
		self.btn_call.clicked.connect(self.send_audio)

		self.show()

	""""
	Despliega los mensajes que se enviaron en la pantalla del chat
	"""
	def show_sending_message(self,message):
		self.txt_message.clear()
		last_message = self.my_user[NAME_CONTACT]+": "+message
		self.txt_conversation.append(last_message)

	""""
	Envia los mensajes al contacto
	"""
	def send_message(self):
		if self.connection_open:
			message = str(self.txt_message.text())
			if len(message) == 0:
				QtGui.QMessageBox.warning(self, WARNING, MISSING_MESSAGE,QtGui.QMessageBox.Ok)
			else:
				try:
					message2 = get_message_header(self.my_user[NAME_CONTACT])+message
					
					self.request_channel.send_text(message2)
					self.show_sending_message(message)
				except Exception as e:
					QtGui.QMessageBox.warning(self, WARNING, CONECTION_FAIL,QtGui.QMessageBox.Ok)	
		else:
			QtGui.QMessageBox.warning(self, WARNING, CONVERSATION_CLOSED,QtGui.QMessageBox.Ok)
	
	""""
	Inicia la llamada
	"""
	def send_audio(self):
		if self.connection_open:
			try:
				self.request_channel.send_audio()
				self.txt_conversation.append(CALLING)
				self.btn_call.hide()
				self.child = CallGUI(self)
				self.request_channel.audio_state(self.my_user[NAME_CONTACT],CALLING)
			except Exception as e:
				QtGui.QMessageBox.warning(self, WARNING, CONECTION_FAIL,QtGui.QMessageBox.Ok)
		else:
			QtGui.QMessageBox.warning(self, WARNING, CONVERSATION_CLOSED,QtGui.QMessageBox.Ok)
			""""
		if not self.channel.send_text(CALLING):
			QtGui.QMessageBox.warning(self, WARNING, CONECTION_FAIL,QtGui.QMessageBox.Ok)
		else:
			self.show_sending_message(CALLING)
			try:
				self.channel.call()
				self.txt_message.setReadOnly(True)
				self.btn_call.hide()
				self.btn_send.hide()
				self.child = CallGUI(self)
			except Exception:
				QtGui.QMessageBox.warning(self, WARNING, CONECTION_FAIL,QtGui.QMessageBox.Ok)
		"""
	""""
	Termina la llamada
	"""
	def end_call(self):
		self.request_channel.stop_sending_audio()
		self.btn_call.show()
		self.btn_send.show()
		self.txt_message.setReadOnly(False)
		self.txt_conversation.append(CALL_END)
		self.request_channel.audio_state(self.my_user[NAME_CONTACT],CALL_END)
		#self.txt_message.setText("LLAMADA TERMINADA")
		#self.send_message()

	
	"""
	Define los eventos que ocurriran cuando se presionen teclas del teclado
	"""
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()
		if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
			self.sendMessage()

	##############################################
	#Muestra los mensajes que le han enviado     #
	##############################################
	def show_receiving_message(self, message):
		self.txt_conversation.append(self.my_contact[NAME_CONTACT]+": "+message)


	def closeEvent(self, evnt):
		if self.connection_open:
			self.my_parent_receiver.close_connection_with(self.my_contact[NAME_CONTACT])
			self.request_channel.remove_connection_with(self.my_user[NAME_CONTACT])

	##############################################
	#Deshabilita los botones e indica al usuario #
	#que el contacto a abandonado la conversación#
	#y no será posible seguir contactandose con  #
	#el a menos a que se establezca una nueva    #
	#conexion                                    #
	##############################################
	def connection_was_closed(self):
		self.connection_open = False
		self.txt_conversation.append(CONNECTION_CLOSED)

	def disable_window(self):
		self.btn_send().setEnabled(False) 
		self.btn_call.setEnabled(False) 
		self.txt_conversation.setEnabled(False) 

	def show_state_audio(self,state):
		self.txt_conversation.append(self.my_contact[NAME_CONTACT]+" -> "+state)


"""
Clase que muestra la pantalla de llamada de voz
"""
class CallGUI(QtGui.QWidget):
	"""
	Constructor
	@param <QWidget> parent: EL widget padre de esta ventana
	"""
	def __init__(self, parent):
		super(CallGUI, self).__init__()
		self.parent = parent
		self.initGUI()
		
	""""
	Inicia los elementos de la GUI, mostrando el texto de Llamada de voz
	"""
	def initGUI(self):		
		#Creación y configuración del widget
		self.setWindowTitle("Llamada")
		self.setGeometry(DEFAULT_POSITION_X, DEFAULT_POSITION_Y, LOGIN_WIDTH, LOGIN_HEIGHT)
		#self.resize(300,200)
		#Configuración layout
		self.grid = QtGui.QGridLayout()
		self.setLayout(self.grid)
		#Declaración elementos de la GUI
		self.lb_my_information = QtGui.QLabel("Llamada de voz",self)
		#Configuración elementos de la GUI		
		self.grid.addWidget(self.lb_my_information,0,0,1,0)

		self.show()

	"""
	Al cerrarse, indica a su padre que la llamada de audio debe terminar
	"""
	def closeEvent(self, event):
		self.parent.end_call()
		event.accept()

	"""
	Define los eventos que ocurriran cuando se presionen teclas
	"""
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()