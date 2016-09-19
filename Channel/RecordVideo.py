#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *
import threading
import multiprocessing as mp
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QImage

import pickle
import cv2

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
	def __init__(self,proxy):
		super(VideoClient, self).__init__()
		self.recording = False
		self.proxy = proxy

	""""
	Captura el video (frame a frame) y lo almacena en una cola
	"""
	def feed_queue(self,q):
		cap = cv2.VideoCapture(0)
		while self.recording:
			ret, frame = cap.read()
			if ret:
				#Codifica el video para enviarlo
				print "Captura actual ENVIADA"
				q.put(pickle.dumps(frame))
		cap.release()
		self.end_call()

	""""
	Inicia la grabación del video, debe correrse en 
	otro hilo para que lo haga de forma constante
	"""
	def init_video(self):
		self.recording = True
		queue = mp.Queue()
		p = threading.Thread(target=self.feed_queue, args=(queue,))
		p.start()
		while self.recording:
			d = queue.get()
			self.proxy.reproduce_video(d)

	"""
	Finaliza el grabado de video
	"""
	def end_call(self):
		self.recording = False
		self.proxy.stop_reproducing()

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
		
	"""
	Reproduce las imagenes que hay en frame
	"""
	def reproduce(self):
		#ventanaImagen = VideoGUI()
		while self.reproducing:
			# Intento de transformar imagen de cv2 a QImage para mostrarla en una ventana de pyqt
			# No funciona, pues parece ser mala idea modificar la GUI desde otro hilo...
			"""
			height, width, channel = self.frame.shape
			bytesPerLine = 3*width
			qImg = QImage(self.frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
			pixmap = QtGui.QPixmap.fromImage(qImg)
			ventanaImagen.imagen.setPixmap(pixmap)
			"""
			cv2.imshow(FRAME_NAME,self.frame)

			if cv2.waitKey(1) & 0xFF == ord('q'): 
				break
		#cv2.destroyAllWindows()
		self.stop_reproducing()
		
	"""
	Finaliza la reproduccion de video
	"""
	def stop_reproducing(self):
		self.reproducing = False
		cv2.destroyAllWindows()

	#Reproduce el video cuando es invocado
	def reproduce_video(self, video):
		#Asigna al frame un valor
		print "Captura actual RECIBIDA"
		self.frame = pickle.loads(video)
		#Si no se está reproduciendo se lanza un hilo para que reproduzca lo que hay en frame
		if not self.reproducing:
			self.reproducing = True
			p = threading.Thread(target=self.reproduce)
			p.start()


"""
Clase auxiliar para mostrar el frame actual del video desde PyQt
"""
class VideoGUI(QtGui.QWidget):
	
	def __init__(self):
		super(VideoGUI, self).__init__()
		self.initGUI()
		
	def initGUI(self):		
		#Creación y configuración del widget
		self.setWindowTitle("VIDEO LLAMADA")
		self.setGeometry(DEFAULT_POSITION_X, DEFAULT_POSITION_Y, LOGIN_WIDTH, LOGIN_HEIGHT)
		#Configuración layout
		self.grid = QtGui.QGridLayout()
		self.setLayout(self.grid)
		#Declaracion de las etiquetas de los elemetos

		#Declaración elementos de la GUI
		self.lb_my_information = QtGui.QLabel("IMAGEN:",self)
		self.imagen = QtGui.QLabel(self)

		#Configuración elementos de la GUI		
		self.grid.addWidget(self.lb_my_information,0,0,1,0)
		self.grid.addWidget(self.imagen,3,0,1,0)

		self.show()

	"""
	Define los eventos que ocurriran cuando se presionen teclas del teclado
	"""
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			# Finalizar video llamada (?)
			self.close()