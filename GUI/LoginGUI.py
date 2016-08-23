#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
#Direcciones relativas
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *
from Constants.AuxiliarFunctions import *
from ChatGUI import ChatGUI
"""
Clase de interfaz grafica que nos permite desplegar la pantalla de logueo
"""
class LoginGUI(QtGui.QWidget):
	
	""""
	mode: Modo de logueo que se va a realizar, sea local
	o remoto
	"""
	def __init__(self,mode=REMOTE):
		super(LoginGUI, self).__init__()
		self.mode = mode
		self.chat = None
		self.initGUI()
		
	""""
	Inicia los elementos de la GUI, solicitando el 
	número del puerto del usuario y el número del
	puerto del contacto o las direccion de ip de contacto
	"""
	def initGUI(self):		
		#Creación y configuración del widget
		self.setWindowTitle(LOGIN_WINDOW)
		self.setGeometry(DEFAULT_POSITION_X, DEFAULT_POSITION_Y, LOGIN_WIDTH, LOGIN_HEIGHT)
		#self.resize(300,200)
		#Configuración layout
		self.grid = QtGui.QGridLayout()
		self.setLayout(self.grid)
		#Declaracion de las etiquetas de los elemetos
		lb_my_title = None
		lb_contac_title = None
		if self.mode in LOCAL:
			lb_my_title = MY_PORT_NUMBER_TITLE
			lb_contac_title = OTHER_PORT_NUMBER_TITLE
		else:
			lb_my_title = MY_IP + get_ip_address()
			lb_contac_title = OTHER_IP_NUMBER_TITLE
		#Declaración elementos de la GUI
		if self.mode in LOCAL:
			self.txt_my_information = QtGui.QLineEdit(self)		
		self.lb_my_information = QtGui.QLabel(lb_my_title,self)
			
		self.lb_contact_information = QtGui.QLabel(lb_contac_title,self)
		self.txt_contact_information = QtGui.QLineEdit(self)

		self.btn_login = QtGui.QPushButton(LOGIN_TITLE,self)

		#Configuración elementos de la GUI 
		
		self.grid.addWidget(self.lb_my_information,0,0,3,0)
		if self.mode in LOCAL:
			self.grid.addWidget(self.txt_my_information,1,0,3,0)
		self.grid.addWidget(self.lb_contact_information,2,0,3,0)
		self.grid.addWidget(self.txt_contact_information,3,0,3,0)
		self.grid.addWidget(self.btn_login,5,2)

		self.btn_login.clicked.connect(self.login)

		self.show()
	
	"""
	Revisa que los campos de texto no esten vacios
	En caso de que la informacion este completa, avanza a la pantalla de chat
	"""
	def login(self):
		complete_information = False
		if self.mode in LOCAL:
			text_my_information = self.txt_my_information.text()
			if len(text_my_information) != 0:
				complete_information = True
		else:
			text_my_information = DEFAULT_PORT
		
		text_my_contact_information = self.txt_contact_information.text()

		if complete_information and len(text_my_contact_information) == 0:
			QtGui.QMessageBox.warning(self, WARNING, INCOMPLETE_INFORMATION,QtGui.QMessageBox.Ok)
		else:
			mode = self.mode
			self.chat = ChatGUI(text_my_information,text_my_contact_information,mode)
			self.close()

	"""
	Define los eventos que ocurriran cuando se presionen teclas del teclado
	"""
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()
		if event.key() == QtCore.Qt.Key_Return:
			self.login()
