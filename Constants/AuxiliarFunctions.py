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




""" Funcion que construira el header del mensaje a mandar """
def get_message_header(username):
	return username+':'


from Constants import *
def split_message_header(message):
	#El mensaje estara sera: username:ip:texto....
	message_split = message.split(':')
	message = ""
	aux = 1
	for i  in message_split:
		if aux != 1:
			message = message + i
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


def codify_password(password):
	newpass = ""
	for letra in password:
		val_ascii = ord(str(letra))
		val_ascii = val_ascii + 5
		newpass = newpass + chr(val_ascii)
	return newpass


def get_method(value):
	message = value.split(METHOD_SEP)
	method = message[0]
	params = message[1:]
	return method,params

def get_message(method,params):
	message = method
	for p in params:
		#print"p= "+str(p)
		message = message + METHOD_SEP+ str(p)

	return message

import time
def send_message_chunks(s,message):
	cont = 0
	chunk = ""
	j = 1
	for i in message:
		
		if cont<BUFFER_SIZE:
			cont +=1

		else:
			cont = 0
			print "Enviando chunk"+chunk
			s.send(chunk)
			chunk = ""

		chunk +=i
		j +=1
		if j > len(message):
			if len(chunk)>0:
				print "Enviando chunk"+chunk
				s.send(chunk)
				time.sleep(0.5)

			print "envien final"
			s.send(FINAL)


