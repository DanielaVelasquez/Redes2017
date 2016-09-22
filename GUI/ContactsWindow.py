#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
#Direcciones relativas
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Channel.DirectoryChannel import DirectoryChannel
from Constants.Constants import *
from Constants.AuxiliarFunctions import *
from Channel.ApiServer import Receiver
"""
Clase de interfaz grafica que permite visualizar los contactos disponibles en el chat
"""
class ContactsWindow(QtGui.QWidget,Receiver):
	"""
	Constructor
	@param <str> my_information: informacion propia para la conexion
    @param <str> my_contact_information: informacion del contacto para la conexion
    @param <str> mode: modo en el que operara el programa (constantes LOCAL o REMOTE)
	"""
	def __init__(self,my_information,my_contact_information,mode,username):
		super(ContactsWindow, self).__init__()

		if mode in LOCAL:
			self.user = dictionaryUser(username,get_ip_address(),my_information)
		else:
			self.user = dictionaryUser(username,my_information,DEFAULT_PORT)

		self.my_contact_information = my_contact_information
		self.mode = mode
		self.directory_channel = None
		self.initGUI()

	
	def initGUI(self):		
		#Creación y configuración del widget
		self.setWindowTitle(CHAT_WINDOW)
		self.setGeometry(DEFAULT_POSITION_X+10, DEFAULT_POSITION_Y+10, CHAT_WIDTH, CHAT_HEIGHT)
		self.resize(500,200)
		#Configuración layout
		self.grid = QtGui.QGridLayout()
		self.setLayout(self.grid)
		#Declaración elementos de la GUI
		self.lb_title_contacts_window = QtGui.QLabel(CONTACT_WINDOW_TITLE,self)
		self.txt_contacts = QtGui.QTextEdit(self)
		self.txt_contacts.setReadOnly(True)
		
		self.btn_refresh = QtGui.QPushButton(REFRESH_TITLE,self)
		#Configuración elementos de la GUI 
		self.grid.addWidget(self.lb_title_contacts_window,0,0)
		self.grid.addWidget(self.txt_contacts,1,0,10,10)
		self.grid.addWidget(self.btn_refresh,12,8,3,2)
		
		self.btn_refresh.clicked.connect(self.updateContacts)

		#try:
		self.connectGeneralDirectory()
		#except Exception, e:
			#QtGui.QMessageBox.warning(self, WARNING, str(e) ,QtGui.QMessageBox.Ok)
		

		self.show()

	#******************************************#
	#Realiza la conexión con el directorio     #
	#general de contactos                      #
	#******************************************#
	def connectGeneralDirectory(self):
		if self.mode in LOCAL:
			self.directory_channel = DirectoryChannel(self, my_port = self.user[PORT_CONTACT], directory_port = self.my_contact_information, username = self.user[NAME_CONTACT])
		else:
			self.directory_channel = DirectoryChannel(self,directory_ip = self.my_contact_information,  username = self.user[NAME_CONTACT])

		self.directory_channel.connect()


	""""
	Despliega los mensajes que se enviaron en la pantalla del chat
	"""
	def showSendingMessage(self,message):
		self.txt_message.clear()
		last_message = "Yo: "+message
		self.txt_contacts.append(last_message)

	""""
	Actualiza los contactos conectados
	"""
	def updateContacts(self):
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
		self.txt_contacts.append("Contacto: "+message)

	"""
	Define los eventos que ocurriran cuando se presionen teclas del teclado
	"""
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()
		if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
			self.sendMessage()
"""
app = QtGui.QApplication(sys.argv)
a = ContactsWindow(None,None,None)
sys.exit(app.exec_())
"""