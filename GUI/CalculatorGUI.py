import sys
from PyQt4 import QtGui

class CalculatorGUI:

	def __init__(self):
		self.initGUI()

	def initGUI(self):
		self.app = QtGui.QApplication([])
		
		#Creación y configuración del widget
		self.widget = QtGui.QWidget()
		self.widget.setWindowTitle('Calculadora')
		self.widget.resize(700,500)
		self.widget.move(500,300)

		#Configuración layout
		self.grid = QtGui.QGridLayout()
		self.widget.setLayout(self.grid)
		
		#Declaración elementos de la GUI
		self.txt_input = QtGui.QLineEdit(self.widget)

		self.btn_numbers = []

		for x in range(0,10):
			self.btn_numbers.append(QtGui.QPushButton(str(x),self.widget))

		self.btn_punto = QtGui.QPushButton(".",self.widget)
		self.btn_igual = QtGui.QPushButton("=",self.widget)
		self.btn_add = QtGui.QPushButton("+",self.widget)
		self.btn_sub = QtGui.QPushButton("-",self.widget)
		self.btn_mul = QtGui.QPushButton("*",self.widget)
		self.btn_div = QtGui.QPushButton("/",self.widget)

		#Configuración elementos de la GUI
		self.grid.addWidget(self.txt_input,1,0,4,-1)
		pos = 7
		for fila in range(2,5): #Ubicación de los botones en el grid
			inicial = pos
			for col in range(0,3):
				self.grid.addWidget(self.btn_numbers[pos],fila,col)
				pos = pos + 1
			pos = inicial - 3

		self.grid.addWidget(self.btn_numbers[0],5,0)
		self.grid.addWidget(self.btn_punto,5,1)
		self.grid.addWidget(self.btn_igual,5,2)
		self.grid.addWidget(self.btn_add,5,3)
		self.grid.addWidget(self.btn_sub,4,3)
		self.grid.addWidget(self.btn_mul,3,3)
		self.grid.addWidget(self.btn_div,2,3)

		self.widget.show()

a = CalculatorGUI()
