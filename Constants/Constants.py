#! /usr/bin/env python


#####################################################
# PURPOSE: Archivo con constantes                   #
#                                                   #
# Vilchis Dominguez Miguel Alonso                   #
#       <mvilchis@ciencias.unam.mx>                 #
#                                                   #
# Notes:                                            #
#                                                   #
# Copyright   16-08-2015                            #
#                                                   #
# Distributed under terms of the MIT license.       #
#####################################################
import pyaudio
CHAT_WIDTH = 500
CHAT_HEIGHT = 500
LOGIN_WIDTH = 250
LOGIN_HEIGTH = 200
CALL_WIDTH = 250
CALL_HEIGTH = 200
DEFAULT_POSTION_X =350
DEFAULT_POSTION_Y =350
INFO_HEIGTH = 40
INFO_WIDTH = CHAT_WIDTH
CHAT_PORT = 5000
### Audio
#TODO 
### Video
#TODO
### Directorio
SERVER_PORT =  7000
MESSAGE_IP = 0
MESSAGE_PORT = 1
MESSAGE_TEXT = 2
WIDGET = 'widget'

NAME_CONTACT = 'username'
IP_CONTACT = 'ip_contact'
PORT_CONTACT = 'port_contact'

TABLE_ITEMS = 2
FIRST_ITEM = 0
SECOND_ITEM = 1


#Nombres para etiquetas login local y remoto
MY_PORT_NUMBER_TITLE = "Cual es mi puerto?:"
OTHER_PORT_NUMBER_TITLE = "Cual es el puerto del directorio general?:"
OTHER_IP_NUMBER_TITLE = "Cual es la direccion IP del directorio general?:"
MY_USER_NAME = "Nombre de usuario"
LOGIN_TITLE = "Acceder"
MY_IP = "Mi IP: "

#Nombres para las etiquetas del chat
CONVERSATION_TITLE = "Conversacion"
SEND_TITLE = "Responder"
CALL_TITLE = "Llamar"

#Titulo de las ventanas GUI
LOGIN_WINDOW = "Login"
CHAT_WINDOW = "Chat"

#Pixeles de las ventanas GUI
DEFAULT_POSITION_X = 100
DEFAULT_POSITION_Y = 100
LOGIN_WIDTH = 300
LOGIN_HEIGHT = 200
CHAT_WIDTH = 500
CHAT_HEIGHT = 600

#Modos de acceso  al chat, local o remoto
LOCAL = "Local"
REMOTE = "Remote"

#Mensajes de error
WARNING = "Alertas"
MISSING_MESSAGE = "No hay ningun mensaje para enviar"

#Localhost
LOCALHOST = "localhost"
DEFAULT_PORT = 5000
LOCALHOST_CLIENT = "localhost"
HTTP = "http://"

#Excepciones
MISSING_WRAPPER = "Falta definir un wrapper que reciba los mensajes del chat"
WRONG_OPTION = "Opcion no valida para iniciar"
PORT_IN_USE = "Ese puerto ya esta en uso, no es posible establecer la conexion"
INCOMPLETE_INFORMATION= "Todos los campos de texto son obligatorios por favor asegurese de llenarlos todos"
CONECTION_FAIL = "No se ha podido establecer la conexion con su contacto"

#Configuracion grabacion audio
CHUNK = 1024
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2

WIDTH_PYAUDIO_FORMAT = 2


FRAME_NAME = 'frame'
EXIT_NUM = 1
EXIT_KEY = 'q'

#DirectoryServer
DEFAULT_PORT_DIRECTORY_SERVER = 6666
USERNAME_USED = "El nombre de usuario ya se encuentra en uso, por favor cambie el nombre de usuario e intente nuevamente"

ERROR_REQUEST_CHANNEL = 'The values of fields are not consistent RequestChannel.__init__'

CONTACT_WINDOW_TITLE = "Contactos conectados"
REFRESH_TITLE = "Actualizar contactos"