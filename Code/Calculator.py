import sys


FILE_NAME = "input.txt"
SEP = " , "

class Calculator(object):

	def __init__(self,first_op=0,second_op=0):
		self.first_operand = first_op
		self.second_operand = second_op

	def add(self):
		return self.first_operand + self.second_operand

	def substract(self):
		return self.first_operand - self.second_operand

	def multiply(self):
		return self.first_operand * self.second_operand

	def divide(self):
		try:
			return self.first_operand / self.second_operand
		except ZeroDivisionError as err:
			return "No se puede dividir entre cero"##CONS_ZERO_DIVISON_ERROR

	def addUser(self,username,password):
		#Revisar si esta registrado
		if self.isRegistred(username):
			return False
		#Convertir password
		newpass = self.changePassword(password)

		archivo = open(FILE_NAME,'a')
		archivo.write("\n"+username + " , "+newpass)
		archivo.close()
		return True

	def login(self, username,password):
		newpass = self.changePassword(password)
		archivo = open(FILE_NAME,'r')
		for line in archivo:
			vals = line.split(SEP,2)
			if(vals[0] == username and vals[1] == newpass):
				return True
		return False

	def changePassword(self, password):
		newpass = ""
		for letra in password:
			val_ascii = ord(letra)
			val_ascii = val_ascii + 5
			newpass = newpass + chr(val_ascii)
		return newpass

	def isRegistred(self,username):
		archivo = open(FILE_NAME,'r')
		for line in archivo:
			vals = line.split(SEP,2)
			if(vals[0] == username):
				return True
		return False
