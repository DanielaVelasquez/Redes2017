#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
#Direcciones relativas
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Channel.DirectoryChannel import DirectoryChannel
from Constants.Constants import *
from Constants.AuxiliarFunctions import *
from Channel.ApiServer import Receiver
"""
Clase de interfaz grafica que permite visualizar los contactos disponibles en el chat
"""
class ContactsWindow(QtGui.QWidget,Receiver):
	"""
	Constructor
	@param <str> my_information: informacion propia para la conexion
    @param <str> my_contact_information: informacion del contacto para la conexion
    @param <str> mode: modo en el que operara el programa (constantes LOCAL o REMOTE)
	"""
	def __init__(self,my_information,my_contact_information,mode,username):
		super(ContactsWindow, self).__init__()

		if mode in LOCAL:
			self.user = dictionaryUser(username,get_ip_address(),my_information)
		else:
			self.user = dictionaryUser(username,my_information,DEFAULT_PORT)

		self.my_contact_information = my_contact_information
		self.mode = mode
		self.directory_channel = None
		self.initGUI()

	
	def initGUI(self):		
		#Creación y configuración del widget
		self.setWindowTitle(CHAT_WINDOW)
		self.setGeometry(DEFAULT_POSITION_X+10, DEFAULT_POSITION_Y+10, CHAT_WIDTH, CHAT_HEIGHT)
		self.resize(500,200)
		#Configuración layout
		self.grid = QtGui.QGridLayout()
		self.setLayout(self.grid)
		#Declaración elementos de la GUI
		self.lb_username = QtGui.QLabel(LB_USERNAME+self.user[NAME_CONTACT],self)
		self.lb_title_contacts_window = QtGui.QLabel(CONTACT_WINDOW_TITLE,self)
		self.txt_contacts = QtGui.QListWidget(self)
		self.txt_contacts.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		#self.txt_contacts.setReadOnly(True)
		
		self.btn_refresh = QtGui.QPushButton(REFRESH_TITLE,self)
		#Configuración elementos de la GUI 
		self.grid.addWidget(self.lb_username,0,0)
		self.grid.addWidget(self.lb_title_contacts_window,1,0)
		self.grid.addWidget(self.txt_contacts,2,0,10,10)
		self.grid.addWidget(self.btn_refresh,12,8,3,2)
		
		self.btn_refresh.clicked.connect(self.updateContacts)

		self.txt_contacts.itemDoubleClicked.connect(self.showContact)

		try:
			self.connectGeneralDirectory()
			self.show()
		except Exception, e:
			QtGui.QMessageBox.warning(self, WARNING, str(e) ,QtGui.QMessageBox.Ok)
		

	def showContact(self):
		print "llegue"
		a = self.txt_contacts..selectedIndexes()
		print "selected: "+str(a)

	#******************************************#
	#Realiza la conexión con el directorio     #
	#general de contactos                      #
	#******************************************#
	def connectGeneralDirectory(self):
		if self.mode in LOCAL:
			self.directory_channel = DirectoryChannel(self, my_port = self.user[PORT_CONTACT], directory_port = self.my_contact_information, username = self.user[NAME_CONTACT])
		else:
			self.directory_channel = DirectoryChannel(self,directory_ip = self.my_contact_information,  username = self.user[NAME_CONTACT])

		self.directory_channel.connect()
		self.updateContacts()

	def updateContacts(self):
		
		contacts = self.directory_channel.get_contacts()
		self.txt_contacts.clear()
		for c in contacts:
			item = QtGui.QListWidgetItem(str(c))
			self.txt_contacts.addItem(item)
		

		


	
"""
app = QtGui.QApplication(sys.argv)
a = ContactsWindow(None,None,None)
sys.exit(app.exec_())
"""