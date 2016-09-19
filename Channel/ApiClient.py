#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.Constants import *
import threading
import multiprocessing as mp

import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import numpy
from RecordAudio import AudioClient
from RecordVideo import VideoClient

"""
Clase MyApiClient que servira como el cliente de cada instancia del programa
"""
class MyApiClient:    
    """
    Constructor de la clase
    @param <int> contact_port: especifica el puerto de contacto del contacto, 
    en caso de no especificarse se toma el puerto por defecto
    @param <str> contact_ip: especifica la ip del contacto en caso de no 
    trabajar de forma local, si no se especfica toma por defecto localhost
    """
    def __init__(self, contact_port,contact_ip):
        if contact_port is None:
            contact_port = DEFAULT_PORT
        if contact_ip is None:
            contact_ip = LOCALHOST_CLIENT
        self.contact_port = contact_port
        self.contact_ip = contact_ip
        self.calling = False
           
    """"
    Envia la peticion de envio del mensaje hacia el servidor que se encuentra conectado
    @param <str> message: mensaje que se desea enviar
    """
    def sendMessage(self,message):
        try:
            self.proxy = xmlrpclib.ServerProxy(HTTP+str(self.contact_ip)+":"+str(self.contact_port)+"/", allow_none=True)
            self.proxy.sendMessage_wrapper(str(message))
            return True
        except Exception, ex:
            return False

    """"
    Inicia la llamada entre los contactos
    """
    def call(self):
        if not self.calling:
            self.calling = True
            self.queue = mp.Queue()
            self.audioRecorder = AudioClient()
            self.p = threading.Thread(target=self.audioRecorder.feed_queque, args=(self.queue,))
            #self.p = mp.Process(target=self.audioRecorder.feed_queque, args=(self.queue,))
            self.p.daemon = True
            self.p.start()
            
            self.proxy = xmlrpclib.ServerProxy(HTTP+str(self.contact_ip)+":"+str(self.contact_port)+"/")
            while self.calling:
                d = self.queue.get()
                data = xmlrpclib.Binary(d)
                self.proxy.playAudio(data)        

    """"
    Termina la llamada
    """
    def end_call(self):
        self.calling = False

    """
    Inicia la video llamada
    """
    def videocall(self):
        #print "Sin crear el proxy"
        self.proxy = xmlrpclib.ServerProxy(HTTP+str(self.contact_ip)+":"+str(self.contact_port)+"/")

        self.video = VideoClient(self.proxy)
        print "Hice un VideoClient con self.proxy"

        self.video_thread = threading.Thread(target=self.video.init_video)
        self.video_thread.daemon = True
        self.video_thread.start()

    """
    Finaliza el envio de audio
    """
    def end_videocall(self):
        self.video.end_call()
