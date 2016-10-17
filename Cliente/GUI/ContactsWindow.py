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
from PyQt4.QtCore import SIGNAL, QObject
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
	def __init__(self,my_information,my_contact_information,mode,username,password, sender = None):
		super(ContactsWindow, self).__init__()

		self.username = username
		self.password = password
		#try:
		if mode in LOCAL:
			self.user = dictionaryUser(username,get_ip_address(),my_information)
		else:
			self.user = dictionaryUser(username,my_information,DEFAULT_PORT)
		
		self.my_contact_information = my_contact_information
		self.mode = mode
		self.directory_channel = None

		self.connect()
		print "sender: "+sender
		if sender == SENDER_REGISTER:
			print "contacts window registrando usuario"
			self.directory_channel.register_user(username,password)
		
		


		#Chats con lo cuales se ha establecido una conexión
		#Se manejara un diccionario de {'nombre_usuario':ventana_chat}
		self.chats = {}
		#Almacena las concecciones cerradas por el contacto, mantiene la ventana del chat abierta
		self.closed_by_contact = {}
		#Nombre del último contacto que pidio hacer conexión
		self.new_contact_window = None

		#Nombre del ultimo contacto cerro la conexion
		self.last_contact_closed = None
		

		self.initGUI()
		
		#except Exception, e:
		#	QtGui.QMessageBox.warning(self, WARNING, str(e) ,QtGui.QMessageBox.Ok)

		
		

	
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
		
		#self.btn_refresh.clicked.connect(self.update_contacts)

		self.txt_contacts.itemDoubleClicked.connect(self.show_contact)

		#self.connect_general_directory()
		self.directory_channel.login(self.username,self.password)
		self.setting_signal()


		self.show()
		
		
	#******************************************#
	#Establece la conexión con el contacto     #
	#******************************************#
	def show_contact(self):
		selected_user = str(self.txt_contacts.currentItem().text())
		#Revisa que no se tenga una ventana con dicho chat
		if self.chats.has_key(selected_user):
			QtGui.QMessageBox.warning(self, WARNING, CHAT_OPEN ,QtGui.QMessageBox.Ok)
		else:
			#Crea conexión
			self.new_window_chat(selected_user)

			#Solicita crea la otra ventana
			chat = self.chats[selected_user]
			chat.connect()

	def add_contact_receiver(self,user):
		self.directory_channel.get_server().get_wrapper().add_contact(user[IP_CONTACT],user[PORT_CONTACT],user[NAME_CONTACT])
	
	def new_window_chat(self,selected_user):
		contacts = self.directory_channel.get_contacts()

		#Si el contacto aún está conectado, dado que la lista
		#no está sincronizada con el servidor, puede que el 
		#contacto ya no esté activo
		if contacts.has_key(selected_user):
			#Crea una ventana de chat para el contacto con el que 
			#se quiere comunicar
			chat = ChatGUI(self.user,contacts[selected_user],self.mode,self)
			self.chats[selected_user] = chat
		else:
			#self.update_contacts()
			QtGui.QMessageBox.warning(self, WARNING, CONECTION_FAIL,QtGui.QMessageBox.Ok)


	#******************************************#
	#Realiza la conexión con el directorio     #
	#general de contactos                      #
	#******************************************#
	def connect_general_directory(self):
		self.directory_channel.connect()
		try:
			
			self.update_contacts()
		except Exception as e:
			pass

	def connect(self):
		if self.mode in LOCAL:
			self.directory_channel = DirectoryChannel(self, my_port = self.user[PORT_CONTACT], directory_port = self.my_contact_information, username = self.user[NAME_CONTACT])
		else:
			self.directory_channel = DirectoryChannel(self,directory_ip = self.my_contact_information,  username = self.user[NAME_CONTACT])

		

	#*******************************************#
	#Actualiza la lista de contactos disponibles#
	#de acuerdo a la información del servidor   # 
	#de usuarios                                #
	#******************************************#
	def update_contacts(self):
		pass
		"""
		contacts = self.directory_channel.get_contacts()
		self.show_contacts(contacts)
		"""

	#Abre una ventana de chat para el contacto que se indicó
	def open_window(self):
		if self.new_contact_window:
			self.new_window_chat(self.new_contact_window)
			self.new_contact_window = None

	#Gestiona para poder recibir la señal
	def setting_signal(self):
		api = self.directory_channel.get_server().get_wrapper()
		QObject.connect(api, SIGNAL(SIGNAL_CREATE_WINDOW),self.open_window, QtCore.Qt.QueuedConnection)

	def closeEvent(self, evnt):
		self.directory_channel.disconnect()

	"""	
	def disable_chat(self):
		if self.last_contact_closed:
			if self.closed_by_contact.has_key(self.last_contact_closed):
				chat = self.closed_by_contact[self.last_contact_closed]
				chat.disable_window()
	"""


	#---------------Métodos heredados---------------------------------
	
	def showNewChat(self, contact_ip, contact_port, username):
		self.new_contact_window = username

	def showMessage(self, user,message):
		if self.chats.has_key(user):
			chat = self.chats[user]
			chat.show_receiving_message(message)

	#Invocado por el chat del usuario que cerró la conexion
	def close_connection_with(self,username):
		if self.chats.has_key(username):
			del self.chats[username]

	#Invocado por el contacto cuando cerró la conexion
	def remove_contact(self,username):
		if self.chats.has_key(username):
			chat = self.chats[username]
			chat.connection_was_closed()
			self.closed_by_contact[username] = chat
			self.close_connection_with(username)

	def state_audio(self,username,state):
	 	if self.chats.has_key(username):
	 		chat = self.chats[username]
	 		chat.show_state_audio(state)

	def show_contacts(self,contacts):
		try:
			self.txt_contacts.clear()
			for c in contacts:
				item = QtGui.QListWidgetItem(str(c))
				self.txt_contacts.addItem(item)
		except Exception as e:
			pass
	 	