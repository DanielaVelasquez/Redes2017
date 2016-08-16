#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from Calculator import Calculator

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *

class ScientificCalculator(Calculator):

	def __init__(self,first_op = float(0),second_op = float(0)):
		super(ScientificCalculator,self).__init__()
		self.first_operand = first_op
		self.second_operand = second_op
	""""
	Calcula el modulo entre los operandos de la calculadora, retorna
	un mensaje de error en caso de que se haga un operacion por 0
	"""
	def module(self):
		try:
			return self.first_operand % self.second_operand
		except ZeroDivisionError as err:
			return CONS_ZERO_DIVISON_ERROR
	"""""
	Calcula la potencia entre los operandos de la calculadora
	"""	
	def pot(self):
		return self.first_operand ** self.second_operand

