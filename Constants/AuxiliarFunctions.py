#! /usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################
# PURPOSE:Funciones auxiliares                      #
#                                                   #
# Vilchis Dominguez Miguel Alonso                   #
#       <mvilchis@ciencias.unam.mx>                 #
#                                                   #
#                                                   #
# Copyright   16-08-2015                            #
#                                                   #
# Distributed under terms of the MIT license.       #
#####################################################
import socket

"""**************************************************
Metodo auxiliar que se conecta a internet para
conocer nuestra ip actual
**************************************************"""
def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return "%s"% (s.getsockname()[0])

"""
Funcion que construye el header del mensaje a mandar
"""
def get_message_header(username):
	return username+':'

from Constants import *

"""
Divide el mensaje en (message_user, message)
"""
def split_message_header(message):
	#El mensaje sera: username:ip:texto
	message_split = message.split(':')
	message = ""
	aux = 1
	for i in message_split:
		if aux != 1:
			message += i
		else:
			aux = 0
	return (message_split[MESSAGE_USER], message)

"""
Crea un diccionario con la información de un usuario
"""
def dictionaryUser(username,ip,port):
	user = {}
	user[NAME_CONTACT] = username
	user[IP_CONTACT] = ip
	user[PORT_CONTACT] = port
	return user

"""
Cifra la contrasenia del usuario
"""
def codify_password(password):
	newpass = ""
	for letra in password:
		val_ascii = ord(str(letra))
		val_ascii = val_ascii + 5
		newpass += chr(val_ascii)
	return newpass

"""
Identifica el metodo y parametros de una llamada
"""
def get_method(value):
	message = value.split(METHOD_SEP)
	method = message[0]
	params = message[1:]
	return method,params

"""
Dado un metodo y sus parametros
Los junta con el formato definido (method$#param1$#param2$#...)
"""
def get_message(method, params):
	message = method
	for p in params:
		message = message+METHOD_SEP+str(p)
	return message

import time

"""
Envia un mensaje a una direccion IP
"""
def send_message_chunks(s, message, ip_addres):
	#print "enviando: "+str(message)
	cont = 0
	#Chunk a enviar
	chunk = ""
	for i in message:
		#Si ya se alcanzó el limite del buffer, se envia el chunk acumulado y se reinicia el conteo
		if len(chunk) == BUFFER_SIZE:
			s.sendto(chunk, ip_addres)
			cont = 0
			chunk = ""
		#Añadir al chunk caracter por caracter
		chunk += i
	#Enviar lo restante del chunk
	if len(chunk) > 0:
		s.sendto(chunk, ip_addres)
	#Enviar comando que indica el final del mensaje ($#@)
	s.sendto(FINAL, ip_addres)

"""
Permite recibir un mensaje, se encarga de cortarlo donde sea necesario (*)
"""
def receieve_message(s, want_message):
	#Chunk recibido
	chunk = ""
	#Mensaje respuesta
	data = ""
	#Mientras no llegue el chunk final
	while chunk != FINAL:
		data +=chunk
		chunk,addr = s.recvfrom(BUFFER_SIZE)
		#Para separar el FINAL del resto del mensaje
		if FINAL in chunk:
			val = chunk
			data += val.replace(FINAL,"")
			chunk = FINAL
	if want_message:
		return data
	else:
		if data != OK:
			raise Exception(data)

"""
Determina si es un audio (*) Deprecated(?)
"""
def is_audio(chunk):
	for i in chunk:
		val_ascii = ord(str(i))
		if val_ascii < 32 or  val_ascii > 126:
			return True
	return False