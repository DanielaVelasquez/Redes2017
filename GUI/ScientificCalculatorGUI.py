#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4.QtGui import *
from ButtonImage import ButtonImage
from AddUserGUI import AddUserGUI

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Code.ScientificCalculator import ScientificCalculator
from Constants.Constants import *


class ScientificCalculatorGUI:

	def __init__(self,cal = ScientificCalculator()):
		self.calculator = cal
		self.wrote = False
		self.initGUI()
		

	def initGUI(self):
		self.app = QtGui.QApplication([])
		
		#Creación y configuración del widget
		self.widget = QtGui.QWidget()
		self.widget.setWindowTitle('Calculadora científica')
		#ancho,alto
		self.widget.resize(100,250)

		#Configuración layout
		self.grid = QtGui.QGridLayout()
		self.widget.setLayout(self.grid)
		
		#Declaración elementos de la GUI
		self.btn_addUser = ButtonImage(QPixmap(IMAGE_LOCATION))

		self.txt_input = QtGui.QLineEdit(self.widget)

		self.btn_numbers = []

		for x in range(0,10):
			btn = QtGui.QPushButton(str(x),self.widget)
			btn.setMaximumWidth(WIDTH_BUTTON)
			self.btn_numbers.append(btn)

		self.btn_punto = QtGui.QPushButton(POINT_SYMBOL,self.widget)
		self.btn_igual = QtGui.QPushButton(EQUAL_SYMBOL,self.widget)
		self.btn_add = QtGui.QPushButton(ADD_SYMBOL,self.widget)
		self.btn_sub = QtGui.QPushButton(SUBSTRACT_SYMBOL,self.widget)
		self.btn_mul = QtGui.QPushButton(MUL_SYMBOL,self.widget)
		self.btn_div = QtGui.QPushButton(DIV_SYMBOL,self.widget)

		self.btn_mod =  QtGui.QPushButton(MODULE_NAME,self.widget)
		self.btn_pot =  QtGui.QPushButton(POT_NAME,self.widget)
		self.btn_clear = QtGui.QPushButton(CLEAR_NAME,self.widget)
		
		#Configuración elementos de la GUI
		
		self.grid.addWidget(self.btn_addUser,0,0,1,1)
		self.btn_addUser.setMaximumWidth(WIDTH_BUTTON_IMG)
		self.btn_addUser.setMaximumHeight(WIDTH_BUTTON_IMG)
		
		self.grid.addWidget(self.txt_input,0,0,4,0)

		pos = 7
		for fila in range(INIT_ROW_NUMBERS,INIT_ROW_NUMBERS + COLS): #Ubicación de los botones en el grid
			inicial = pos
			for col in range(0,COLS):
				self.grid.addWidget(self.btn_numbers[pos],fila,col)
				pos = pos + 1
			pos = inicial - 3

		self.grid.addWidget(self.btn_numbers[0],6,0)
		self.btn_numbers[0].setMaximumWidth(WIDTH_BUTTON)

		self.grid.addWidget(self.btn_punto,6,1)
		self.btn_punto.setMaximumWidth(WIDTH_BUTTON)

		self.grid.addWidget(self.btn_igual,6,2)
		self.btn_igual.setMaximumWidth(WIDTH_BUTTON)

		self.grid.addWidget(self.btn_add,6,3)
		self.btn_add.setMaximumWidth(WIDTH_BUTTON)

		self.grid.addWidget(self.btn_sub,5,3)
		self.btn_sub.setMaximumWidth(WIDTH_BUTTON)

		self.grid.addWidget(self.btn_mul,4,3)
		self.btn_mul.setMaximumWidth(WIDTH_BUTTON)

		self.grid.addWidget(self.btn_div,3,3)
		self.btn_div.setMaximumWidth(WIDTH_BUTTON)

		self.grid.addWidget(self.btn_mod,7,0)
		self.btn_mod.setMaximumWidth(WIDTH_BUTTON)

		self.grid.addWidget(self.btn_pot,7,1)
		self.btn_pot.setMaximumWidth(WIDTH_BUTTON)

		self.grid.addWidget(self.btn_clear,7,2)
		self.btn_clear.setMaximumWidth(WIDTH_BUTTON)

		#Configuración de los eventos
		buttons = self.btn_numbers
		buttons.append(self.btn_punto)
		buttons.append(self.btn_add)
		buttons.append(self.btn_sub)
		buttons.append(self.btn_mul)
		buttons.append(self.btn_div)
		buttons.append(self.btn_pot)
		buttons.append(self.btn_mod)

		for but in buttons:
			but.clicked.connect(self.displayText)

		self.btn_igual.clicked.connect(self.operate)

		self.txt_input.textChanged.connect(self.onTextChanged)
		self.btn_addUser.clicked.connect(self.newUser)
		self.btn_clear.clicked.connect(self.clear)

		self.newAddUser = None 

		self.widget.show()
		#sys.exit(self.app.exec_())

	def clear(self):
		self.txt_input.clear()

	def onTextChanged(self):
		text = self.txt_input.text()
		if self.wrote and len(text)!=0:
			val = text[len(text)-1]
			self.txt_input.setText(val)
			self.wrote = False
			

		if EQUAL_SYMBOL in text:
			self.deleteLasDigit()
			self.operate()

	def deleteLasDigit(self):
		text = self.txt_input.text()
		val = text[0:len(text)-1]
		self.txt_input.setText(val)
		
	def newUser(self):
		self.newAddUser = AddUserGUI(self.calculator)
		self.widget.close()

	def displayText(self):

		if self.wrote:
			self.txt_input.setText("")
			self.wrote = False

		button = self.widget.sender()
		value = button.text()

		self.txt_input.setText(self.txt_input.text() + value)
		

	def operate(self):
		text = self.txt_input.text()
		operator = ""
		operate = True
		if DIV_SYMBOL in text:
			operator = DIV_SYMBOL
		elif MUL_SYMBOL in text:
			operator = MUL_SYMBOL
		elif SUBSTRACT_SYMBOL in text:
			operator = SUBSTRACT_SYMBOL
		elif ADD_SYMBOL in text:
			operator = ADD_SYMBOL
		elif MODULE_NAME in text:
			operator = MODULE_NAME
		elif POT_NAME in text:
			operator = POT_NAME
		else:
			self.txt_input.setText(INVALID_OPERATION)
			operate = False

		if operate:
			nums = text.split(operator,2)
			try:
				first = float(nums[0])
				second = float(nums[1])

				self.calculator.first_operand = first
				self.calculator.second_operand = second
				
				resultado = None

				if DIV_SYMBOL in operator:
					resultado = self.calculator.divide()
				elif MUL_SYMBOL in operator:
					resultado = self.calculator.multiply()
				elif SUBSTRACT_SYMBOL in operator:
					resultado = self.calculator.substract()
				elif ADD_SYMBOL in operator:
					resultado = self.calculator.add()
				elif MODULE_NAME in operator:
					resultado = self.calculator.module()
				else:
					resultado = self.calculator.pot()
				self.txt_input.setText(str(resultado))

			except ValueError:
				self.txt_input.setText(INVALID_OPERATION)

		self.wrote = True
#a = ScientificCalculatorGUI()
