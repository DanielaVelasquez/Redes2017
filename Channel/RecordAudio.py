#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pyaudio
import numpy
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *
from Constants.AuxiliarFunctions import *
import xmlrpclib
import socket

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
    def __init__(self, s = None):
        super(AudioClient, self).__init__()
        self.calling = False
        self.socket = s

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
                frame.append(self.stream.read(CHUNK))
            data_ar = numpy.fromstring(''.join(frame),  dtype=numpy.uint8)
            queque.put(data_ar)

    def callback_function(self, in_data, frame_count, time_info, flag):
        audio_data = numpy.fromstring(in_data, dtype = numpy.float32)
        self.socket.sendall(audio_data)
        return (audio_data, pyaudio.paContinue)

    def record(self):
        p = pyaudio.PyAudio()
        self.calling = True
        FORMAT = p.get_format_from_width(2)
        self.stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK,
                            stream_callback = self.callback_function)
        self.stream.start_stream()
        while self.calling:
            time.sleep(0.1)

from cStringIO import StringIO
from numpy.lib import format

#####################################################
# Clase encargada de la reproduccion del audio      #
# que reciba de su contacto del chat                #
# Idea tomada de repositorio github:                #
#     https://github.com/mvilchis/redes-17_Ejemplos #
#####################################################
class AudioServer(object):

    def __init__(self):
        super(AudioServer, self).__init__()
        self.p = pyaudio.PyAudio()
        self.FORMAT = self.p.get_format_from_width(2)
        self.stream = self.p.open(format=self.FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            output=True,
                            frames_per_buffer=CHUNK)        

    def playAudio(self,audio):
        self.stream.write(audio)