#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pyaudio
import numpy
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *

#####################################################
# Clase encargada de la grabación del audio         #
# entre los usuarios conectados                     #
# Idea tomada de repositorio github:                #
#     https://github.com/mvilchis/redes-17_Ejemplos #
#####################################################
class AudioClient(object):
	
	""""
	Inicia el objeto cliente que es capaz de realizar la grabación
	del audio 
	"""
	def __init__(self):
		super(RecordAudioClient, self).__init__()
		
	""""
	Método que se encarga de estar grabando de forma continua el audio y encolarlo.

	"""	
	def feed_queque(self, queque):
		#Inicia la configuración para la grabación del audio
		self.pyaudio = pyaudio.PyAudio()
		self.pyaudio_format = self.pyaudio.get_format_from_width(WIDTH_PYAUDIO_FORMAT)

		self.stream = self.pyaudio.open(format=self.pyaudio_format, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

		while True:
			frame = []
	        for i in range(0,int(RATE/CHUNK *RECORD_SECONDS)):
	            frame.append(stream.read(CHUNK))
	        data_ar = numpy.fromstring(''.join(frame),  dtype=numpy.uint8)
	        queque.put(data_ar)
#####################################################
# Clase encargada de la reproduccion del audio      #
# que reciba de su contacto del chat                #
# Idea tomada de repositorio github:                #
#     https://github.com/mvilchis/redes-17_Ejemplos #
#####################################################

from cStringIO import StringIO
from numpy.lib import format

class AudioServer(object):

	def __init__(self, arg):
		super(AudioServer, self).__init__()

	def toArray(self,s):
	    f=StringIO(s)
	    arr=format.read_array(f)
	    return arr 

	def playAudio(self,audio):
	    p = pyaudio.PyAudio()
	    FORMAT = p.get_format_from_width(2)
	    stream = p.open(format=FORMAT,
	                    channels=CHANNELS,
	                    rate=RATE,
	                    output=True,
	                    frames_per_buffer=CHUNK)

	    data = audio.data
	    stream.write(data)
	    stream.close()
	    p.terminate()

	def reproduce(self):
	    while True:
	        if len(frames) > 0:
	            cv2.imshow('Servidor',frames.pop(0))
	            if cv2.waitKey(1) & 0xFF==ord('q'):
	                break
	    cv2.destroyAllWindows()

	
