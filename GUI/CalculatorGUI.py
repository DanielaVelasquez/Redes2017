import sys
from PyQt4 import QtGui
from PyQt4.QtGui import *
from ButtonImage import ButtonImage

WIDTH_BUTTON = 64
WIDTH_BUTTON_IMG = 32
POINT_SYMBOL = "."
ADD_SYMBOL = "+"
SUBSTRACT_SYMBOL = "-"
DIV_SYMBOL = "/"
MUL_SYMBOL = "*"
EQUAL_SYMBOL = "="
IMAGE_LOCATION = "icon/add-user.png"
INIT_ROW_NUMBERS = 3
COLS = 3

class CalculatorGUI:

	def __init__(self):
		self.initGUI()

	def initGUI(self):
		self.app = QtGui.QApplication([])
		
		#Creación y configuración del widget
		self.widget = QtGui.QWidget()
		self.widget.setWindowTitle('Calculadora')
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

		self.widget.show()

a = CalculatorGUI()
