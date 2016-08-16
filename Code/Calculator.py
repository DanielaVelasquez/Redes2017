#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Constants.Constants import *

class Calculator(object):

	def __init__(self,first_op=0,second_op=0):
		self.first_operand = first_op
		self.second_operand = second_op

	""""
	Realiza la suma entre los dos operando
	"""
	def add(self):
		return self.first_operand + self.second_operand
	""""
	Realiza la resta entre los dos operando
	"""	
	def substract(self):
		return self.first_operand - self.second_operand
	""""
	Realiza la multiplicacion entre los dos operando
	"""
	def multiply(self):
		return self.first_operand * self.second_operand
	""""
	Realiza la division entre los dos operando y en caso
	de presentarse una division por cero retorna un mensaje de error
	"""
	def divide(self):
		try:
			return self.first_operand / self.second_operand
		except ZeroDivisionError as err:
			return CONS_ZERO_DIVISON_ERROR
	""""
	Permite el registro de usuarios para que puedan utilizar la calculadora,
	a partir de un nombre de usuario y una contraseña
	"""
	def addUser(self,username,password):
		#Revisar si esta registrado
		
		if self.isRegistred(username):
			return False
		#Convertir password
		newpass = self.changePassword(password)
		archivo = open(FILE_NAME,'a')
		
		archivo.write(username + " , "+newpass+"\n")
		archivo.close()
		return True
	""""
	Verifica si existe un usuario registrado con las credenciales
	indicadad (username, password) y dice si puede o no acceder a
	la calculadora
	"""
	def login(self, username,password):
		newpass = self.changePassword(password) + "\n"

		archivo = open(FILE_NAME,'r')
		for line in archivo:
			vals = line.split(SEP,2)
			if(vals[0] == username and vals[1] == newpass):
				return True
		return False

	""""
	Codifica una contraseña añadiendo a cada caracter de la cadena
	5 unidades en su representacion ascii
	"""
	def changePassword(self, password):
		newpass = ""
		for letra in password:
			val_ascii = ord(str(letra))
			val_ascii = val_ascii + 5
			newpass = newpass + chr(val_ascii)
		return newpass
	""""
	Determina si un usuario se nombre de usuario ya ha sido
	previamente registrado
	"""
	def isRegistred(self,username):
		archivo = open(FILE_NAME,"r")
		for line in archivo:
			vals = line.split(SEP,2)
			if(vals[0] == username):
				return True
		return False

