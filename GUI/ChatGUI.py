#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
#Direcciones relativas
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

#from Channel.Channel import Channel
from Constants.Constants import *
from Constants.AuxiliarFunctions import *
from Channel.ApiServer import FunctionWrapper
"""
Clase de interfaz grafica que permite visualizar la conversacion con el contacto del chat
Y enviar nuevos mensajes por medio de un campo de texto
"""
class ChatGUI(QtGui.QWidget,FunctionWrapper):
	"""
	Constructor
	@param <str> my_information: informacion propia para la conexion
    @param <str> my_contact_information: informacion del contacto para la conexion
    @param <str> mode: modo en el que operara el programa (constantes LOCAL o REMOTE)
	"""
	def __init__(self,my_information,my_contact_information,mode):
		super(ChatGUI, self).__init__()
		self.my_information = my_information
		self.my_contact_information = my_contact_information
		self.mode = mode
		self.channel = None
		#self.makeConnection()
		self.initGUI()

	"""""
	Crea el canal de conexion y establece la conexion
	con el contacto de acuerdo a los datos entregados por
	el usuario
	"""
	def makeConnection(self):
		if self.mode in LOCAL:
			self.channel = Channel(contact_ip =get_ip_address(),my_port=self.my_information,contact_port=self.my_contact_information)
		else:
			print "chanel make connetion contact_ip ="+str(self.my_contact_information)
			self.channel = Channel(contact_ip = self.my_contact_information)

		self.channel.setWrapper(self)
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

		self.btn_send.clicked.connect(self.sendMessage)
		self.btn_call.clicked.connect(self.call)

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
		message = str(self.txt_message.text())
		if len(message) == 0:
			QtGui.QMessageBox.warning(self, WARNING, MISSING_MESSAGE,QtGui.QMessageBox.Ok)
		else:
			if not self.channel.send_text(message):
				QtGui.QMessageBox.warning(self, WARNING, CONECTION_FAIL,QtGui.QMessageBox.Ok)
			else:
				self.showSendingMessage(message)		
	
	""""
	Inicia la llamada
	"""
	def call(self):
		if not self.channel.send_text("LLAMANDO"):
			QtGui.QMessageBox.warning(self, WARNING, CONECTION_FAIL,QtGui.QMessageBox.Ok)
		else:
			self.showSendingMessage("LLAMANDO")
			try:
				self.channel.call()
				self.txt_message.setReadOnly(True)
				self.btn_call.hide()
				self.btn_send.hide()
				self.child = CallGUI(self)
			except Exception:
				QtGui.QMessageBox.warning(self, WARNING, CONECTION_FAIL,QtGui.QMessageBox.Ok)

	""""
	Termina la llamada
	"""
	def end_call(self):
		self.channel.end_call()
		self.btn_call.show()
		self.btn_send.show()
		self.txt_message.setReadOnly(False)
		self.txt_message.setText("LLAMADA TERMINADA")
		self.sendMessage()

	"""
	Muestra el mensaje del contacto (manteniendo la conversacion)
	"""
	def sendMessage_wrapper(self, message):
		self.txt_conversation.append("Contacto: "+message)

	"""
	Define los eventos que ocurriran cuando se presionen teclas del teclado
	"""
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()
		if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
			self.sendMessage()
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