import sys
sys.path.insert(0,'Redes2017/Constants/Constants')
##import Constants

class Calculator:

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

""""
a = Calculator()
a.first_operand = 2
a.second_operand = 0
print("%d" % (a.divide()))
"""