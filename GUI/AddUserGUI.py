#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Code.Calculator import Calculator
from Code.ScientificCalculator import ScientificCalculator
from Constants.Constants import *
from Code import *

class AddUserGUI():


	def __init__(self,cal):
		self.calculator = cal
		self.initGUI()
	""""
	Inicia los elementos de la GUI 
	"""
	def initGUI(self):
		self.app = QtGui.QApplication([])
		
		#Creación y configuración del widget
		self.widget = QtGui.QWidget()
		self.widget.setWindowTitle(TITLE_ADD_USER)
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

		self.btn_add = QtGui.QPushButton(TITLE_ADD_USER,self.widget)

		#self.btn_back = QtGui.QPushButton(TITLE_BACK,self.widget)

		#Configuración elementos de la GUI 
		self.grid.addWidget(self.lb_user,0,0)
		self.grid.addWidget(self.txt_user,0,1)
		self.grid.addWidget(self.lb_pass,1,0)
		self.grid.addWidget(self.txt_pass,1,1)
		self.grid.addWidget(self.btn_add,2,1)
		#self.grid.addWidget(self.btn_back,2,0)

		self.txt_pass.setEchoMode(QtGui.QLineEdit.Password)

		#Configuración eventos
		self.btn_add.clicked.connect(self.newUser)
		#self.btn_back.clicked.connect(self.goBack)
		self.calculatorGUI = None

		self.widget.show()

	""""
	Realiza el llamado a la calculadora para registrar un nuevo 
	usuario, previamente verificando que ninguno de los campos 
	este vacio
	"""	
	def newUser(self):
		user = self.txt_user.text()
		pas = self.txt_pass.text()

		if len(user) ==0 or len(pas) ==0:
			QtGui.QMessageBox.warning(self.widget, WARNING, ICOMPLETE_INFORMATION,QtGui.QMessageBox.Ok)
		elif self.calculator.addUser(user,pas):
			QtGui.QMessageBox.information(self.widget, INFORMATION,SUCCESFUL_REGISTRATION ,QtGui.QMessageBox.Ok)
			self.txt_user.clear()
			self.txt_pass.clear()
		else:
			QtGui.QMessageBox.warning(self.widget, WARNING, "El usuario con nombre "+user+" ya esta registrado",QtGui.QMessageBox.Ok)