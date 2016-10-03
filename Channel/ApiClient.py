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
            contact_ip = get_ip_address()
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
            self.proxy.sendMessage_wrapper(message)
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
            self.p.daemon = True
            self.p.start()
            
            if self.proxy is None:
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
        if self.proxy is None:
            self.proxy = xmlrpclib.ServerProxy(HTTP+str(self.contact_ip)+":"+str(self.contact_port)+"/")
        
        print "Mandamos al servidor a esperar los frames"
        self.proxy.reproduce_video()

        self.video = VideoClient(self.proxy)
        # Comenzamos a enviar los frames
        self.video.init_video()

    """
    Finaliza el envio de audio
    """
    def end_videocall(self):
        if self.video is None:
            self.video = VideoClient(self.proxy)
        self.video.end_call()
