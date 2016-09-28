#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Constants.Constants import *
from Constants.AuxiliarFunctions import *
from ContactsWindow import ContactsWindow

class Register(QtGui.QWidget):

	def __init__(self,mode=None):
		super(Register, self).__init__()
		self.mode = mode
		self.directory = None
		self.initGUI()
	""""
	Inicia los elementos de la GUI 
	"""
	def initGUI(self):
		
		#Creación y configuración del widget
		
		self.setWindowTitle(TITLE_ADD_USER)
		self.resize(250,150)
		#self.move(500,300)
		
		#Configuración layout
		self.grid = QtGui.QGridLayout()
		self.setLayout(self.grid)

		title_directory = None
		title_my_information = None
		if self.mode == LOCAL:
			title_directory = OTHER_PORT_NUMBER_TITLE
			title_my_information = MY_PORT_NUMBER_TITLE
		else:
			title_directory = OTHER_IP_NUMBER_TITLE
			title_my_information = MY_IP

		#Declaración elementos de la GUI
		self.lb_user = QtGui.QLabel(TITLE_USER,self)
		self.lb_pass = QtGui.QLabel(TITLE_PASS,self)
		self.lb_pass_confirm = QtGui.QLabel(CONF_PASS,self)
		self.lb_directory = QtGui.QLabel(title_directory,self)
		self.lb_my_information = QtGui.QLabel(title_my_information,self)

		self.txt_user = QtGui.QLineEdit(self)
		self.txt_pass = QtGui.QLineEdit(self)
		self.txt_pass_confrm = QtGui.QLineEdit(self)
		self.txt_directory = QtGui.QLineEdit(self)
		self.txt_my_information = QtGui.QLineEdit(self)

		if self.mode ==REMOTE:
			self.txt_my_information.setReadOnly(True)
			self.txt_my_information.setText(get_ip_address())

		self.btn_add = QtGui.QPushButton(TITLE_ADD_USER,self)

		#self.btn_back = QtGui.QPushButton(TITLE_BACK,self)

		#Configuración elementos de la GUI 
		self.grid.addWidget(self.lb_user,0,0)
		self.grid.addWidget(self.txt_user,0,1)
		self.grid.addWidget(self.lb_pass,1,0)
		self.grid.addWidget(self.txt_pass,1,1)
		self.grid.addWidget(self.lb_pass_confirm,2,0)
		self.grid.addWidget(self.txt_pass_confrm,2,1)
		self.grid.addWidget(self.lb_directory,3,0)
		self.grid.addWidget(self.txt_directory,3,1)
		self.grid.addWidget(self.lb_my_information,4,0)
		self.grid.addWidget(self.txt_my_information,4,1)
		self.grid.addWidget(self.btn_add,5,1)

		#self.grid.addWidget(self.btn_back,2,0)

		self.txt_pass.setEchoMode(QtGui.QLineEdit.Password)
		self.txt_pass_confrm.setEchoMode(QtGui.QLineEdit.Password)

		#Configuración eventos
		self.btn_add.clicked.connect(self.create_user)
		
		
		self.show()

	""""
	Realiza el llamado a la calculadora para registrar un nuevo 
	usuario, previamente verificando que ninguno de los campos 
	este vacio
	"""	
	
	def create_user(self):
		user = str(self.txt_user.text())
		pas = str(self.txt_pass.text())
		conf = str(self.txt_pass_confrm.text())
		directory = str(self.txt_directory.text())
		my_information = str(self.txt_my_information.text())

		#Si las contraseñas no coinciden
		if pas != conf:
			QtGui.QMessageBox.warning(self, WARNING, PASSWORD_PROBLEM,QtGui.QMessageBox.Ok)
		#Si hay algun campo vacio
		elif len(user) ==0 or len(pas) ==0 or len(directory) ==0 or len(my_information)==0:
			QtGui.QMessageBox.warning(self, WARNING, INCOMPLETE_INFORMATION,QtGui.QMessageBox.Ok)
		#De lo contrario tratará de establecer la conexión
		else:
			#try:
			#Codifica la contraseña
			password = codify_password(pas)
			
			self.contact_window = ContactsWindow(my_information,directory,self.mode,user,password, sender = SENDER_REGISTER)
		#except Exception as e:
			#	QtGui.QMessageBox.warning(self, WARNING, e.message,QtGui.QMessageBox.Ok)
		

app = QtGui.QApplication(sys.argv)		
a = Register(mode = LOCAL)
sys.exit(app.exec_())