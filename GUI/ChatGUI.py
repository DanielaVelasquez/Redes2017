#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtGui

#Direcciones relativas
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *
from Channel.ApiServer import FunctionWrapper
from Channel.Channel import Channel

class ChatGUI(FunctionWrapper):
	
	def __init__(self,my_information,my_contact_information,mode):
		super(ChatGUI, self).__init__()
		self.my_information = my_information
		self.my_contact_information = my_contact_information
		self.mode = mode
		self.channel = None
		self.makeConnection()
		self.initGUI()

	"""""
	Crea el canal de coneccion y establece la coneccion 
	con el contacto de acuerdo a los datos entregados por
	el usuario
	"""
	def makeConnection(self):
		if self.mode in LOCAL:
			self.channel = Channel(my_port=self.my_information,contact_port=self.my_contact_information)
		else:
			self.channel = Channel(contact_ip = self.my_information)
		self.channel.setWrapper(self)
		self.channel.init_chat()

	""""
	Inicia los elementos de la GUI, mostrando la ventana
	donde se reciben los mensaje y una que permite enviar
	los mensajes
	"""
	def initGUI(self):
		#self.app = QtGui.QApplication([])
		
		#Creación y configuración del widget
		self.widget = QtGui.QWidget()
		self.widget.setWindowTitle(CHAT_WINDOW)
		self.widget.resize(500,200)

		#Configuración layout
		self.grid = QtGui.QGridLayout()
		self.widget.setLayout(self.grid)

		#Declaración elementos de la GUI
		self.lb_conversation = QtGui.QLabel(CONVERSATION_TITLE,self.widget)

		self.txt_conversation = QtGui.QTextEdit(self.widget)
		self.txt_conversation.setReadOnly(True)
		self.txt_message = QtGui.QTextEdit(self.widget)

		self.btn_send = QtGui.QPushButton(SEND_TITLE,self.widget)
		
		#Configuración elementos de la GUI 
		self.grid.addWidget(self.lb_conversation,0,0)
		self.grid.addWidget(self.txt_conversation,1,0,10,10)
		
		self.grid.addWidget(self.txt_message,11,0,5,1)
		self.grid.addWidget(self.btn_send,12,5,3,1)

		self.btn_send.clicked.connect(self.sendMesssage)

		self.widget.show()
		#sys.exit(self.app.exec_())

	"""""
	Despliega los mensaje que se enviaron en la pantalla del chat
	"""
	def showSendingMesssage(self,message):
		self.txt_message.clear()
		self.txt_conversation.append("Yo: message")

	"""""
	Envia los mensajes al contacto
	"""
	def sendMesssage(self):
		message = self.txt_message.toPlainText()
		if len(message) == 0:
			QtGui.QMessageBox.warning(self.widget, WARNING, MISSING_MESSAGE,QtGui.QMessageBox.Ok)
		else:
			if not self.channel.send_text(message):
				QtGui.QMessageBox.warning(self.widget, WARNING, CONECTION_FAIL,QtGui.QMessageBox.Ok)
			else:
				self.showSendingssMesssage(message)
	def sendMessage_wrapper(self, message):
		self.txt_conversation.append("Contacto dice: "+message)
		
