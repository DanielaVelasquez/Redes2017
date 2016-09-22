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
from ChatGUI import ChatGUI
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
		#Chats con lo cuales se ha establecido una conexión
		#Se manejara un diccionario de {'nombre_usuario':ventana_chat}
		self.chats = {}

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
		
		self.btn_refresh.clicked.connect(self.update_contacts)

		self.txt_contacts.itemDoubleClicked.connect(self.show_contact)

		try:
			self.connect_general_directory()
			self.show()
		except Exception, e:
			QtGui.QMessageBox.warning(self, WARNING, str(e) ,QtGui.QMessageBox.Ok)
		
	#******************************************#
	#Establece la conexión con el contacto     #
	#******************************************#
	def show_contact(self):
		selected_user = str(self.txt_contacts.currentItem().text())
		print "Selected user: "+selected_user
		#Revisa que no se tenga una ventana con dicho chat
		if self.chats.has_key(selected_user):
			QtGui.QMessageBox.warning(self, WARNING, CHAT_OPEN ,QtGui.QMessageBox.Ok)
		else:
			print "Cretating window chat with "+selected_user
			#Crea conexión
			self.new_window_chat(selected_user)

			#Solicita crea la otra ventana
			chat = self.chats[selected_user]
			chat.connect()
	
	def new_window_chat(self,selected_user):
		contacts = self.directory_channel.get_contacts()

		#Si el contacto aún está conectado, dado que la lista
		#no está sincronizada con el servidor, puede que el 
		#contacto ya no esté activo
		if contacts.has_key(selected_user):
			print "Contact "+selected_user+" found"
			#Crea una ventana de chat para el contacto con el que 
			#se quiere comunicar
			chat = ChatGUI(self.user,contacts[selected_user],self.mode)
			self.chats[selected_user] = chat
			print "Added to chats: "+str(self.chats)
		else:
			self.update_contacts()
			QtGui.QMessageBox.warning(self, WARNING, CONECTION_FAIL,QtGui.QMessageBox.Ok)


	#******************************************#
	#Realiza la conexión con el directorio     #
	#general de contactos                      #
	#******************************************#
	def connect_general_directory(self):
		if self.mode in LOCAL:
			self.directory_channel = DirectoryChannel(self, my_port = self.user[PORT_CONTACT], directory_port = self.my_contact_information, username = self.user[NAME_CONTACT])
		else:
			self.directory_channel = DirectoryChannel(self,directory_ip = self.my_contact_information,  username = self.user[NAME_CONTACT])

		self.directory_channel.connect()
		self.update_contacts()

	#*******************************************#
	#Actualiza la lista de contactos disponibles#
	#de acuerdo a la información del servidor   # 
	#de usuarios                                #
	#******************************************#
	def update_contacts(self):
		contacts = self.directory_channel.get_contacts()
		self.txt_contacts.clear()
		for c in contacts:
			item = QtGui.QListWidgetItem(str(c))
			self.txt_contacts.addItem(item)

	#---------------Métodos heredados---------------------------------
	
	def showNewChat(self, contact_ip, contact_port, username):
		self.new_window_chat(username)
