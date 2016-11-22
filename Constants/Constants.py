#! /usr/bin/env python
# -*- coding: utf-8 -*-

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


### Directorio
SERVER_PORT =  7000
MESSAGE_IP = 0
MESSAGE_PORT = 1
MESSAGE_TEXT = 1

MESSAGE_USER = 0

WIDGET = 'widget'

NAME_CONTACT = 'username'
IP_CONTACT = 'ip_contact'
PORT_CONTACT = 'port_contact'
CHANNEL_CONTACT = 'channel_contact'
SOCKET_CONTACT = 'socket_channel'

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
CONECTION_FAIL = "No se ha podido establecer la conexion con el contacto"

#Configuracion grabacion audio
CHUNK = 1024
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2

WIDTH_PYAUDIO_FORMAT = 2

# Video

FRAME_NAME = 'frame'
EXIT_NUM = 1
EXIT_KEY = 'q'

#DirectoryServer
DEFAULT_PORT_DIRECTORY_SERVER = 6666
USERNAME_USED = "El usuario se encuentra conectado, por favor cierre otras sesiones"

ERROR_REQUEST_CHANNEL = 'The values of fields are not consistent RequestChannel.__init__'

CONTACT_WINDOW_TITLE = "Contactos conectados"
REFRESH_TITLE = "Actualizar contactos"
LB_USERNAME = "Nombre de usuario: "

CHAT_OPEN = "Ya existe una conversacion abierta con el usuario"

SIGNAL_CREATE_WINDOW = "create_window"
SIGNAL_DISABLE_WINDOW = "disable_window"

CONNECTION_CLOSED = "El contacto abandono la conversacion, no es posible continuar con la transferencia de informacion, inicie una nueva conversacion para esto"

CALLING = "ENVIANDO AUDIO"
CALL_END = "FIN ENVIO AUDIO"

#Registrar usuario
TITLE_USER = "Usuario"
TITLE_ADD_USER = "Nuevo usuario"
TITLE_PASS = "Password"
INFORMATION = "Informacion"
SUCCESFUL_REGISTRATION = "Usuario registrado con exito"
CONF_PASS = "Confirmar password"

PASSWORD_PROBLEM = "Las contraseñas no coinciden"
FILE_NAME = "input.txt"
SEP = " : "

USERNAME_REGISTERED ="El nombre de usuario ya existe"
ERROR_REGISTERING = "El usuario no pudo ser registrado"

SLEEP = 5

REGISTER = "Registrar"

SENDER_REGISTER ="registrar"
SENDER_LOGIN = "iniciar_sesion"

USER_DATA_WRONG = "Datos de usuario no encontrados o incorrectoss"
DEFAULT_PORT_2 = 7000

CONVERSATION_CLOSED = "La comunicación ha terminado, por favor una nuevamente"

#Sockets
BUFFER_SIZE = 20
METHOD_SEP = "$#"
BUFFER_SIZE_C = 20

FINAL = "$#@"

SEP_LIST = "#"
METHOD_NOT_REGISTERED = "Method no registered"

OK = "Ok"