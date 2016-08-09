import sys
from Calculator import Calculator

class ScientificCalculator(Calculator):

	def __init__(self,first_op = float(0),second_op = float(0)):
		super(ScientificCalculator,self).__init__()
		self.first_operand = first_op
		self.second_operand = second_op

	def module(self):
		try:
			return self.first_operand % self.second_operand
		except ZeroDivisionError as err:
			return "Resultado indefinido"##CONS_ZERO_MODULE_ERROR
		
	def pot(self):
		return self.first_operand ** self.second_operand


"""
a = ScientificCalculator()
a.first_operand = 4.2
a.second_operand = 3
print("%s" % (a.add()))
""