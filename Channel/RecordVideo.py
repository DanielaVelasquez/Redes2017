#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Constants.Constants import *

from cStringIO import StringIO
import cv2
from numpy.lib import format
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QImage
import time
import threading
import xmlrpclib

import socket
import struct
#import pickle Quizas lo de pickle en el servidor de video, y no en ApiServer

#####################################################
# Clase encargada de la grabación del video         #
# entre los usuarios conectados                     #
# Idea tomada de repositorio github:                #
#     https://github.com/mvilchis/redes-17_Ejemplos #
#####################################################
class VideoClient(object):
	"""
	Constructor de la clase
	"""
	def __init__(self, s = None):
		super(VideoClient, self).__init__()
		self.calling = False
		self.cap = None
		self.socket = s

	""""
	Captura el video (frame a frame) y lo envia al servidor
	"""
	def record(self):
		self.cap = cv2.VideoCapture(0)
		self.calling = True
		while True:
			ret, frame = self.cap.read()
			# Para mostrar la imagen del lado del cliente
			cv2.imshow('Cliente',frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			data = pickle.dumps(frame)
		self.socket.sendall(struct.pack("L", len(data)) + data)
		self.cap.release()
		cv2.destroyAllWindows()
		self.socket.close()

#####################################################
# Clase encargada de la reproduccion del video      #
# que reciba de su contacto del chat                #
# Idea tomada de repositorio github:                #
#     https://github.com/mvilchis/redes-17_Ejemplos #
#####################################################
class VideoServer(object):
	"""
	Constructor de la clase
	"""
	def __init__(self):
		super(VideoServer, self).__init__()
		self.frame = None

	"""
	Reproduce las imagenes que hay en frame
	"""
	def reproduce(self, frame):
		cv2.imshow('Servidor', frame)
		cv2.waitKey(10)