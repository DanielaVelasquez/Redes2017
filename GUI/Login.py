import sys
from PyQt4 import QtGui

class Login():

	def __init__(self):
		self.initGUI()

	def initGUI(self):
		self.app = QtGui.QApplication([])
		
		#Creación y configuración del widget
		self.widget = QtGui.QWidget()
		self.widget.setWindowTitle('Login')
		self.widget.resize(250,150)
		self.widget.move(500,300)

		#Configuración layout
		self.grid = QtGui.QGridLayout()
		self.widget.setLayout(self.grid)

		#Declaración elementos de la GUI
		self.lb_user = QtGui.QLabel("Usuario",self.widget)
		self.lb_pass = QtGui.QLabel("Password",self.widget)

		self.txt_user = QtGui.QLineEdit(self.widget)
		self.txt_pass = QtGui.QLineEdit(self.widget)

		self.btn_login = QtGui.QPushButton('Ingresar',self.widget)

		#Configuración elementos de la GUI 
		self.grid.addWidget(self.lb_user,0,0)
		self.grid.addWidget(self.txt_user,0,1)
		self.grid.addWidget(self.lb_pass,1,0)
		self.grid.addWidget(self.txt_pass,1,1)
		self.grid.addWidget(self.btn_login,2,1)

		self.widget.show()

	#def login(self):

		
a = Login()

