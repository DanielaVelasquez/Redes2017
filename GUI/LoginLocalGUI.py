#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

#Direcciones relativas
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *

class LoginLocaGUI(object):
	
	def __init__(self):
		super(LoginLocaGUI, self).__init__()
		self.initGUI()

	""""
	Inicia los elementos de la GUI, solicitando el 
	número del puerto del usuario y el número del
	puerto del contacto 
	"""
	def initGUI(self):
		self.app = QtGui.QApplication([])
		
		#Creación y configuración del widget
		self.widget = QtGui.QWidget()
		self.widget.setWindowTitle(LOGIN_WINDOW)
		self.widget.resize(300,200)

		#Configuración layout
		self.grid = QtGui.QGridLayout()
		self.widget.setLayout(self.grid)

		#Declaración elementos de la GUI
		self.lb_my_port = QtGui.QLabel(MY_PORT_NUMBER_TITLE,self.widget)
		self.lb_contact_port = QtGui.QLabel(OTHER_PORT_NUMBER_TITLE,self.widget)

		self.txt_my_port = QtGui.QLineEdit(self.widget)
		self.txt_contact_port = QtGui.QLineEdit(self.widget)

		self.btn_login = QtGui.QPushButton(LOGIN_TITLE,self.widget)

		#Configuración elementos de la GUI 
		self.grid.addWidget(self.lb_my_port,0,0,3,0)
		self.grid.addWidget(self.txt_my_port,1,0,3,0)
		self.grid.addWidget(self.lb_contact_port,2,0,3,0)
		self.grid.addWidget(self.txt_contact_port,3,0,3,0)
		self.grid.addWidget(self.btn_login,5,2)

		self.txt_contact_port.setEchoMode(QtGui.QLineEdit.Password)
		#self.btn_login.clicked.connect(self.login)

		self.widget.show()
		sys.exit(self.app.exec_())

a = LoginLocaGUI()

