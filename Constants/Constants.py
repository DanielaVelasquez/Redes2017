#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Nombres para etiquetas login local y remoto
MY_PORT_NUMBER_TITLE = "Cual es mi puerto?:"
OTHER_PORT_NUMBER_TITLE = "Cual es el puerto de contacto?:"
OTHER_IP_NUMBER_TITLE = "Cual es la direccion IP del contacto?:"
LOGIN_TITLE = "Acceder"
MY_IP = "Mi IP: "

#Nombres para las etiquetas del chat
CONVERSATION_TITLE = "Conversacion"
SEND_TITLE = "Responder"
CALL_TITLE = "Llamar"
VIDEOCALL_TITLE = "Videollamar"
ENDVIDEOCALL_TITLE = "Colgar"

#Titulo de las ventanas GUI
LOGIN_WINDOW = "Login"
CHAT_WINDOW = "Chat"

#Pixeles de las ventanas GUI
DEFAULT_POSITION_X = 100
DEFAULT_POSITION_Y = 100
LOGIN_WIDTH = 300
LOGIN_HEIGHT = 200
CHAT_WIDTH = 500
CHAT_HEIGHT = 800

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

# Configuración grabación audio
CHUNK = 1024
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2
WIDTH_PYAUDIO_FORMAT = 2

# Configuracion grabacion video
FRAME_NAME = 'frame'
EXIT_NUM = 1
EXIT_KEY = 'q'
