#! /usr/bin/env python
# -*- coding: utf-8 -*-


#####################################################
# PURPOSE:Ejemplo de audio con tpc                  #
#                                                   #
# Vilchis Dominguez Miguel Alonso                   #
#       <mvilchis@ciencias.unam.mx>                 #
#                                                   #
# Notes:                                            #
#                                                   #
# Copyright   28-09-2015                            #
#                                                   #
# Distributed under terms of the MIT license.       #
#####################################################

"""
Servidor que por localhost al recibir una peticion
de reproduce el audio
"""

import socket
import pyaudio
""" Constantes de audio """
CHUNK = 1024
CHANNELS = 1
RATE = 44100
""" Constantees de tpc """
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

my_socket = ''
frames = []


def main ():
    global my_socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    my_socket.bind((TCP_IP, TCP_PORT))
    #my_socket.listen(1)
    #conn, addr = my_socket.accept()

    pyaudio_instance = pyaudio.PyAudio()
    FORMAT = pyaudio_instance.get_format_from_width(2)
    stream = pyaudio_instance.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

    while True:
        data, addr = my_socket.recvfrom(CHUNK * CHANNELS * 2)
        if not data: break
        stream.write(data)
    conn.close()

main()