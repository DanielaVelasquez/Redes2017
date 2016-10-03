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

def toString(data):
    f= StringIO()
    format.write_array(f,data)
    return f.getvalue()

def toArray(s):
    f = StringIO(s)
    arr = format.read_array(f)
    return arr

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
	def __init__(self, proxy):
		super(VideoClient, self).__init__()
		self.recording = False
		self.proxy = proxy

	""""
	Captura el video (frame a frame) y lo envia al servidor
	"""
	def feed_queue(self):
		cap = cv2.VideoCapture(0)
		while self.recording:
			ret, frame = cap.read()
			if ret:
				data = xmlrpclib.Binary(toString(frame))
				time.sleep(0.25) # Para limitar los frames enviados por segundo
				self.proxy.my_play_video(data)
				print "Frame actual ENVIADO"
		cap.release()
		self.end_call()

	""""
	Alimenta de frames al servidor, debe correrse en 
	otro hilo para que lo haga de forma constante
	"""
	def init_video(self):
		self.recording = True
		p = threading.Thread(target=self.feed_queue)
		#p.daemon = True
		p.start()

	"""
	Finaliza el grabado de video
	"""
	def end_call(self):
		self.recording = False

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
		#Variable indica si se está reproduciendo el video
		self.reproducing = False
		self.frame = None
		self.frames = []

	"""
	Reproduce las imagenes que hay en frame
	"""
	def reproduce(self):
		print "COMENZANDO Reproduccion de frames"
		while True:
			if len(self.frames) > 0:				
				self.frame = self.frames.pop(0)
				try:
					cv2.imshow('frame', self.frame)
				except Exception:
					print "*** Error al mostrar frame ***"
					cv2.destroyAllWindows()
					reproducing = False
					self.frames = []
				if 0xFF == ord('q'):
					reproducing = False
					self.frames = []
					cv2.destroyAllWindows()

	""" 
	Funcion que sera llamada como procedimiento remoto 
	y agregara el item a la cola 
	"""
	def my_play_video(self, frame):
		if len(self.frames) < 5: # Para evitar overflow del arreglo y carga de trabajo
			self.frames.append(toArray(frame.data))

	"""
	Finaliza la reproduccion de video
	"""
	def stop_reproducing(self):
		self.reproducing = False

	"""
	Crea el thread de reproduccion de video
	"""
	def reproduce_video(self):
		self.reproducing = True
		p = threading.Thread(target=self.reproduce)
		#p.daemon = True
		p.start()