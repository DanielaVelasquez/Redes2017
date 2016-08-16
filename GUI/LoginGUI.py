#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

#Direcciones relativas
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *

class LoginGUI(object):
	
	""""
	mode: modo de logueo que se va a realizar, sea local
	o remoto
	"""
	def __init__(self,mode=REMOTE):
		super(LoginGUI, self).__init__()
		self.mode = mode
		self.initGUI()
		

	""""
	Inicia los elementos de la GUI, solicitando el 
	número del puerto del usuario y el número del
	puerto del contacto o las direccion de ip de contacto
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

		#Declaracion de las etiquetas de los elemetos
		lb_my_title = None
		lb_contac_title = None
		if self.mode in LOCAL:
			lb_my_title = MY_PORT_NUMBER_TITLE
			lb_contac_title = OTHER_PORT_NUMBER_TITLE
		else :
			lb_my_title = MY_IP_NUMBER_TITLE
			lb_contac_title = OTHER_IP_NUMBER_TITLE


		#Declaración elementos de la GUI
		self.lb_my_information = QtGui.QLabel(lb_my_title,self.widget)
		self.lb_contact_information = QtGui.QLabel(lb_contac_title,self.widget)

		self.txt_my_information = QtGui.QLineEdit(self.widget)
		self.txt_contact_information = QtGui.QLineEdit(self.widget)

		self.btn_login = QtGui.QPushButton(LOGIN_TITLE,self.widget)

		#Configuración elementos de la GUI 
		self.grid.addWidget(self.lb_my_information,0,0,3,0)
		self.grid.addWidget(self.txt_my_information,1,0,3,0)
		self.grid.addWidget(self.lb_contact_information,2,0,3,0)
		self.grid.addWidget(self.txt_contact_information,3,0,3,0)
		self.grid.addWidget(self.btn_login,5,2)

		#self.btn_login.clicked.connect(self.login)

		self.widget.show()
		sys.exit(self.app.exec_())

a = LoginGUI(LOCAL)
