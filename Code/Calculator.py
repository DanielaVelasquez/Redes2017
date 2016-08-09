import sys

class Calculator:

	def __init__(self):
		self.primer_operando = 0
		self.segundo_operando = 0

	def add(self):
		return self.primer_operando + self.segundo_operando

	def substract(self):
		return self.primer_operando - self.segundo_operando

	def multiply(self):
		return self.primer_operando * self.segundo_operando

	def divide(self):
		try:
			return self.primer_operando / self.segundo_operando
		except ZeroDivisionError as err:
			return "No se puede dividir entre cero"
