#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Code.ScientificCalculator import ScientificCalculator
from CalculatorGUI import CalculatorGUI

class Login(CalculatorGUI):

	def __init__(self):
		self.calculator = ScientificCalculator()
		#self.initGUI()

a = Login()

