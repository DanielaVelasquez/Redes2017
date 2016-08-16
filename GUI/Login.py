#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Code.ScientificCalculator import ScientificCalculator
from Constants.Constants import *
from ScientificCalculatorGUI import ScientificCalculatorGUI

class Login():

	def __init__(self):
		self.calculator = ScientificCalculator()
		self.initGUI()

	""""
	Inicia los elementos de la GUI
	"""

	def initGUI(self):
		self.app = QtGui.QApplication([])
		
		#Creación y configuración del widget
		self.widget = QtGui.QWidget()
		self.widget.setWindowTitle(TITLE_LOGIN)
		self.widget.resize(250,150)
		self.widget.move(500,300)

		#Configuración layout
		self.grid = QtGui.QGridLayout()
		self.widget.setLayout(self.grid)

		#Declaración elementos de la GUI
		self.lb_user = QtGui.QLabel(TITLE_USER,self.widget)
		self.lb_pass = QtGui.QLabel(TITLE_PASS,self.widget)

		self.txt_user = QtGui.QLineEdit(self.widget)
		self.txt_pass = QtGui.QLineEdit(self.widget)

		self.btn_login = QtGui.QPushButton(TITLE_IN,self.widget)

		#Configuración elementos de la GUI 
		self.grid.addWidget(self.lb_user,0,0)
		self.grid.addWidget(self.txt_user,0,1)
		self.grid.addWidget(self.lb_pass,1,0)
		self.grid.addWidget(self.txt_pass,1,1)
		self.grid.addWidget(self.btn_login,2,1)

		self.txt_pass.setEchoMode(QtGui.QLineEdit.Password)
		self.btn_login.clicked.connect(self.login)

		self.calculatorGUI = None

		self.widget.show()
		sys.exit(self.app.exec_())

	""""
	Llama a la funcion de iniciar sesion de la calculadora
	con la informacion que se encuentra en las cajas de texto,
	previamente verificando que estas no se encuentren vacias
	"""

	def login(self):
		user = self.txt_user.text()
		pas = self.txt_pass.text()
		

		if len(user) ==0 or len(pas) ==0:
			QtGui.QMessageBox.warning(self.widget, WARNING, ICOMPLETE_INFORMATION,QtGui.QMessageBox.Ok)
		elif self.calculator.login(user,pas):
			self.calculatorGUI = ScientificCalculatorGUI(self.calculator)
			self.widget.close()
			#self.widget.close()
		else:
			QtGui.QMessageBox.warning(self.widget, WARNING, INCORRECT_LOGIN,QtGui.QMessageBox.Ok)


		


