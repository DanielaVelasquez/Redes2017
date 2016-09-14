#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *

import pickle
import threading
import multiprocessing as mp
import cv2

class VideoClient(object):
	"""docstring for VideoClient"""
	def __init__(self,proxy):
		super(VideoClient, self).__init__()
		self.reproducing = False
		self.proxy = proxy

	""""
	Captura el video y lo adiciona a una cola
	"""
	def feed_queue(self,q):
		cap = cv2.VideoCapture(0)
		while True:

			ret, frame = cap.read()
			if ret:
				#Codifica el video para enviarlo
				q.put(pickle.dumps(frame))

	""""
	Inicia la grabación del video, debe correrse en 
	otro hilo para que lo haga de forma constante
	"""
	def init_video(self):
		queue = mp.Queue()
		p = threading.Thread(target=feed_queue, args=(queue,))
		p.start()
		self.reproducing = True
		while self.reproducing:
			d = queue.get()
			self.proxy.reproduce_video(d)

	def end_call(self):
		self.reproducing = False
		self.proxy.stop_reproducing()



class VideoServer(object):
	
	def __init__(self):
		super(Video, self).__init__()
		#Variable indica si se está reproduciendo el video
		self.reproducing = False
		self.frame = None
		

	#Reproduce las imagenes que hay en frame
	def reproduce(self):
		while self.reproducing:
			cv2.imshow(FRAME_NAME,self.frame)
		

	def stop_reproducing(self):
		self.reproducing = False
		cv2.destroyAllWindows()

	#Reproduce el video cuando es invocado
	def reproduce_video(self, video):
		#Asigna al frame un valor
		self.frame = pickle.loads(video)
		#Si no se está reproduciendo se lanza un hilo para que reproduzca lo que hay en frame
		if not self.reproducing:
			self.reproducing = True
			p = threading.Thread(target=self.reproduce)
			p.start()

				
