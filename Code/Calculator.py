import sys

class Calculator:

	def __init__(self):
		primer_operando = 0
		segundo_operando = 0

	def add(self):
		return primer_operando + segundo_operando

	def substract(self):
		return primer_operando - segundo_operando

	def multiply(self):
		return primer_operando * segundo_operando

	def divide(self):
		try:
			return primer_operando / segundo_operando
		except ZeroDivisionError as err:
			return "No se puede dividir entre cero"


	