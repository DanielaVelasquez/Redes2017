#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

#Direcciones relativas
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *
from ChatGUI import ChatGUI
from Constants.AuxiliarFunctions import *
class LoginGUI(object):
	
	""""
	mode: modo de logueo que se va a realizar, sea local
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
		#self.app = QtGui.QApplication([])
		
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
			lb_my_title = MY_IP + get_ip_address()
			lb_contac_title = OTHER_IP_NUMBER_TITLE


		#Declaración elementos de la GUI
		if self.mode in LOCAL:
			self.txt_my_information = QtGui.QLineEdit(self.widget)
		
		self.lb_my_information = QtGui.QLabel(lb_my_title,self.widget)
			
		self.lb_contact_information = QtGui.QLabel(lb_contac_title,self.widget)

		self.txt_contact_information = QtGui.QLineEdit(self.widget)

		self.btn_login = QtGui.QPushButton(LOGIN_TITLE,self.widget)

		#Configuración elementos de la GUI 
		if self.mode in LOCAL:
			self.grid.addWidget(self.txt_my_information,1,0,3,0)
		
		self.grid.addWidget(self.lb_my_information,0,0,3,0)
		self.grid.addWidget(self.lb_contact_information,2,0,3,0)
		self.grid.addWidget(self.txt_contact_information,3,0,3,0)
		self.grid.addWidget(self.btn_login,5,2)

		self.btn_login.clicked.connect(self.login)

		self.txt_contact_information.setText("5000")
		self.txt_my_information.setText("8000")

		self.widget.show()
		#sys.exit(self.app.exec_())
	
	def login(self):
		complete_information = False
		if self.mode in LOCAL:
			text_my_information = self.txt_my_information.text()
			if len(text_my_information) !=0:
				complete_information = True
		else:
			text_my_information = DEFAULT_PORT
		
		text_my_contact_information = self.txt_contact_information.text()

		if complete_information and len(text_my_contact_information)==0:
			QtGui.QMessageBox.warning(self.widget, WARNING, INCOMPLETE_INFORMATION,QtGui.QMessageBox.Ok)
		else:
			mode = self.mode
			self.chat = ChatGUI(text_my_information,text_my_contact_information,mode)
			self.widget.close()

