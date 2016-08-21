#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
from Constants.Constants import *
from Channel.Channel import Channel
#Direcciones relativas
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
"""
Clase de interfaz grafica que permite visualizar la conversacion con el contacto del chat
Y enviar nuevos mensajes por medio de un campo de texto
"""
class ChatGUI(QtGui.QWidget):
	
	"""
	Constructor
	"""
	def __init__(self,my_information,my_contact_information,mode):
		super(ChatGUI, self).__init__()
		self.my_information = my_information
		self.my_contact_information = my_contact_information
		self.mode = mode
		self.channel = None
		self.makeConnection()
		self.initGUI()

	"""""
	Crea el canal de conexion y establece la conexion
	con el contacto de acuerdo a los datos entregados por
	el usuario
	"""
	def makeConnection(self):
		if self.mode in LOCAL:
			self.channel = Channel(my_port=self.my_information,contact_port=self.my_contact_information)
		else:
			self.channel = Channel(contact_ip = self.my_information)
		self.channel.setWrapper(self) # Khe?.... bueno, lo dejare asi
		self.channel.init_chat()

	""""
	Inicia los elementos de la GUI, mostrando la ventana
	donde se reciben los mensaje y una que permite enviar
	los mensajes
	"""
	def initGUI(self):		
		#Creación y configuración del widget
		self.setWindowTitle(CHAT_WINDOW)
		self.setGeometry(DEFAULT_POSITION_X+10, DEFAULT_POSITION_Y+10, CHAT_WIDTH, CHAT_HEIGHT)
		self.resize(500,200)
		#Configuración layout
		self.grid = QtGui.QGridLayout()
		self.setLayout(self.grid)
		#Declaración elementos de la GUI
		self.lb_conversation = QtGui.QLabel(CONVERSATION_TITLE,self)
		self.txt_conversation = QtGui.QTextEdit(self)
		self.txt_conversation.setReadOnly(True)
		self.txt_message = QtGui.QTextEdit(self)
		self.btn_send = QtGui.QPushButton(SEND_TITLE,self)		
		#Configuración elementos de la GUI 
		self.grid.addWidget(self.lb_conversation,0,0)
		self.grid.addWidget(self.txt_conversation,1,0,10,10)		
		self.grid.addWidget(self.txt_message,11,0,5,1)
		self.grid.addWidget(self.btn_send,12,5,3,1)

		self.btn_send.clicked.connect(self.sendMessage)

		self.show()

	""""
	Despliega los mensajes que se enviaron en la pantalla del chat
	"""
	def showSendingMessage(self,message):
		self.txt_message.clear()
		last_message = "Yo: "+message
		self.txt_conversation.append(last_message)

	""""
	Envia los mensajes al contacto
	"""
	def sendMessage(self):
		message = self.txt_message.toPlainText()
		if len(message) == 0:
			QtGui.QMessageBox.warning(self, WARNING, MISSING_MESSAGE,QtGui.QMessageBox.Ok)
		else:
			if not self.channel.send_text(message):
				QtGui.QMessageBox.warning(self, WARNING, CONECTION_FAIL,QtGui.QMessageBox.Ok)
			else:
				self.showSendingMessage(message)
	"""
	Wrapper
	"""
	def sendMessage_wrapper(self, message):
		self.txt_conversation.append("Contacto dice: "+message)

	"""
	Define los eventos que ocurriran cuando se presionen teclas del teclado
	"""
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()
		if event.key() == QtCore.Qt.Key_Return:
			self.sendMessage()
