#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#Direcciones relativas
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *
from Constants.AuxiliarFunctions import *
from ContactsWindow import ContactsWindow
#from Register import Register
"""
Clase de interfaz grafica que nos permite desplegar la pantalla de logueo
"""
class LoginGUI(QtGui.QWidget):
	
	""""
	mode: Modo de logueo que se va a realizar, sea local
	o remoto
	"""
	
	def __init__(self,my_information=None,my_contact_information=None,mode=REMOTE,username = None):
		super(LoginGUI, self).__init__()
		self.mode = mode
		self.contacts_window = None
		if my_information and my_contact_information and username:
			self.contacts_window = ContactsWindow(my_information,my_contact_information,mode,username)
		else:
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
		self.lb_user = QtGui.QLabel(TITLE_USER,self)
		self.lb_pass = QtGui.QLabel(TITLE_PASS,self)
		self.txt_user = QtGui.QLineEdit(self)
		self.txt_pass = QtGui.QLineEdit(self)

		self.lb_my_information = QtGui.QLabel(lb_my_title,self)
		if self.mode in LOCAL:
			self.txt_my_information = QtGui.QLineEdit(self)		
			
		self.lb_contact_information = QtGui.QLabel(lb_contac_title,self)
		self.txt_contact_information = QtGui.QLineEdit(self)

		self.btn_login = QtGui.QPushButton(LOGIN_TITLE,self)

		self.btn_register = QtGui.QPushButton(REGISTER,self)

		#Configuración elementos de la GUI		
		self.grid.addWidget(self.lb_my_information,0,0,1,0)
		if self.mode in LOCAL:
			self.grid.addWidget(self.txt_my_information,1,0,1,0)
		self.grid.addWidget(self.lb_contact_information,2,0,1,0)
		self.grid.addWidget(self.txt_contact_information,3,0,1,0)

		self.grid.addWidget(self.lb_user,5,0,1,0)
		self.grid.addWidget(self.txt_user,6,0,1,0)

		self.grid.addWidget(self.lb_pass,7,0,1,0)
		self.grid.addWidget(self.txt_pass,8,0,1,0)

		self.grid.addWidget(self.btn_login,9,1)
		self.grid.addWidget(self.btn_register,10,1)

		self.btn_login.clicked.connect(self.login)
		self.btn_register.clicked.connect(self.register)

		self.txt_pass.setEchoMode(QtGui.QLineEdit.Password)

		self.show()


	def register(self):
		pass
		#register = Register(self.mode)
		#register.show()
		#self.close()
	
	"""
	Revisa que los campos de texto no esten vacios
	En caso de que la informacion este completa, avanza a la pantalla de chat
	"""
	def login(self):
		complete_information = False
		if self.mode in LOCAL:
			text_my_information = self.txt_my_information.text()
			
			if len(text_my_information) != 0 :
				complete_information = True
		else:
			text_my_information = DEFAULT_PORT
		
		text_my_contact_information = str(self.txt_contact_information.text())
		text_username = str(self.txt_user.text())
		text_password = str(self.txt_pass.text())
		
		if not complete_information and len(text_my_contact_information) == 0 and len(text_username) == 0 and len(text_password)==0:
			QtGui.QMessageBox.warning(self, WARNING, INCOMPLETE_INFORMATION,QtGui.QMessageBox.Ok)
		else:
			mode = self.mode
			password = codify_password(text_password)
			#print "text_my_information "+text_my_information+"\ntext_my_contact_information "+text_my_contact_information+"\ntext_username "+text_username+"\n"+mode
			self.contacts_window = ContactsWindow(my_information = text_my_information,my_contact_information=text_my_contact_information,mode=mode,username=text_username,password=password, sender = SENDER_LOGIN)
			self.close()

	"""
	Define los eventos que ocurriran cuando se presionen teclas del teclado
	"""
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()
		if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
			self.login()
