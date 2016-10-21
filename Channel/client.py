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
Cliente por localhost que después de conectarse
manda audio
"""
import socket
import pyaudio
import numpy as np
import time

""" Constantes de audio """
CHUNK = 1024
CHANNELS = 1
RATE = 44100
""" Constantes de tpc """
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20

my_socket = ''
"""
def callback_function(in_data, frame_count, time_info, flag):
        global my_socket,TCP_PORT,TCP_IP
        audio_data = np.fromstring(in_data, dtype=np.float32)
        send_message_chunks(my_socket,str(audio_data),(TCP_IP, TCP_PORT))
        return (audio_data, pyaudio.paContinue)
"""
def callback_function(in_data, frame_count, time_info, flag):
        global my_socket,TCP_PORT,TCP_IP
        audio_data = np.fromstring(in_data, dtype=np.float32)
        my_socket.sendto(audio_data,(TCP_IP,TCP_PORT))
        #send_message_chunks(my_socket,(audio_data),(TCP_IP, TCP_PORT))
 
        return (audio_data, pyaudio.paContinue)

def main ():
    global my_socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    my_socket.connect((TCP_IP, TCP_PORT))
    pyaudio_instance = pyaudio.PyAudio()
    FORMAT = pyaudio_instance.get_format_from_width(2)
    stream = pyaudio_instance.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback = callback_function)
    stream.start_stream()
    while True:
        time.sleep(0.1)

    my_socket.close()

main()