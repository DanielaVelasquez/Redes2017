#! /usr/bin/env python
# -*- coding: utf-8 -*-


#####################################################
# PURPOSE: Clase que manejara los clientes que se   #
#          conectan y desconectan al sistema        #
#                                                   #
# Vilchis Dominguez Miguel Alonso                   #
#       <mvilchis@ciencias.unam.mx>                 #
#                                                   #
# Notes:                                            #
#                                                   #
# Copyright   17-08-2015                            #
#                                                   #
# Distributed under terms of the MIT license.       #
#####################################################
import socket
#           Mis bibliotecas
import sys,getopt
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Constants.AuxiliarFunctions import *
from Constants.Constants import *
from Channel.Channels import RequestChannel
import threading
import time


class GeneralDirectory:
    """ Constructor de la clase, si recibe un puerto, entonces
        Trabajara de manera local, de otra manera, utilizará  la ip
        con la que cuenta.
        @param port <int> Si trabaja de manera local, representa el
                        número del puerto por el cual recibirá las peticiones
    """
    def __init__(self, port = DEFAULT_PORT):
        self.client_dictionary = {}
        TCP_IP = get_ip_address()
        TCP_PORT = int(port)
        
        #Inicia el servidor
        self.port = port

        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((TCP_IP, TCP_PORT))
        self.s.listen(1)

        self.funtionWrapper = FunctionWrapperDirectory(self.client_dictionary)
        print ("Directorio de ubicacion activo, mi direccion es:")
        print ("(%s, %s))" %(get_ip_address(), port))

        
        conn,addr = self.s.accept()

        while(1):
            data = conn = recv(BUFFER_SIZE)
            if not data:
                break
            if data:
                method, params = get_method(data)
                if method == 'connect_wrapper':
                    self.funtionWrapper.connect_wrapper(params[0],params[1],params[2])
                elif method == 'disconnect_wrapper':
                    self.funtionWrapper.disconnect_wrapper(params[0])
                elif method == 'register':
                    self.funtionWrapper.register(params[0],params[1])
                elif method == 'login':
                    self.funtionWrapper.login(params[0],params[1],params[2],params[3])
                elif method == 'sendMessage_wrapper':
                    self.funtionWrapper.sendMessage_wrapper(params[0])
                elif method == 'play_audio_wrapper':
                    self.funtionWrapper.play_audio_wrapper(params[0])
                elif method == 'update_contacts':
                    self.funtionWrapper.update_contacts(params[0])
                else:
                    print data+"Not registered"
        



class FunctionWrapperDirectory:
    """ **************************************************
    Constructor de la clase
    @clients_dictionary (Diccionario) Contiene la información de
                todos los clientes (Usa username como llave, y contiene el nombre del usuario)
    ************************************************** """
    def __init__(self,client_dictionary):
        self.client_dictionary = client_dictionary
        self.registered_users = {}
        self.read_users()
        self.start_thread()

    def start_thread(self):
        self.update_thread = threading.Thread(target = self.update) 
        self.update_thread.daemon = True
        self.update_thread.start()

    def update(self):
        while True:
            try:
                for user in self.client_dictionary:
                    d = self.client_dictionary[user]
                    channel = d[CHANNEL_CONTACT]
                    c = self.get_contacts_wrapper(user)
                    try:
                        channel.send_contacts(c)
                    except Exception as e:
                        print "Error: "+str(e)
                        self.disconnect_wrapper(user)
            except Exception as e:
                pass
            #print "usuarios registrados: "+str(self.registered_users)+"\n"
            #print "usuarios conectados: "+str(self.client_dictionary)
                
            time.sleep(SLEEP)

    def read_users(self):
        archivo = open(FILE_NAME,'r')
        print "Usuarios registrados"
        for line in archivo:
            l = line.split(SEP,2)
            username = l[0]
            password = l[1]
            print "username: "+username+" password: "+password
            self.registered_users[username] = password
        #print "usuarios registrados: "+str(self.registered_users)

    def is_registered(self, username):
        return self.registered_users.has_key(username)

    def register(self, username,password):
        print "Registrando "+username
        if self.is_registered(username):
            raise Exception(USERNAME_REGISTERED)
        else:
            try:
                password = password +"\n"
                archivo = open(FILE_NAME,'a')
                archivo.write(username+SEP+password)
                self.registered_users[username] = password
            except Exception:
                raise Exception(ERROR_REGISTERING)

    def get_contacts_wrapper(self,  username):
        #Se clona el diccionario de usuarios
        print "getting contacts "+str(username)
        copy = self.client_dictionary.copy()
        #Se elimina el usuario solicitó información
        if self.client_dictionary.has_key(username):
            del copy[username]
            for u in copy:
                inf = copy[u].copy()
                del inf[CHANNEL_CONTACT]
                copy[u] = inf
            return copy
        #TODO
    """"********************************************
    Adiciona un nuevo contacto
    *********************************************"""
    def connect_wrapper(self, ip_string, port_string, username):
        print "Iniciando usuario: "+username
        print "usuarios conectados: "+str(self.client_dictionary)
        print "->self.client_dictionary.has_key(username)"+str(self.client_dictionary.has_key(username))
        #Revisa si existe un usuario con dicho nombre
        if self.client_dictionary.has_key(username):
            #No permite la conexión
            print "Usuario conectado"
            raise Exception(USERNAME_USED)
        else:
            user = self.user_to_dictionary(username,ip_string,port_string)
            self.client_dictionary[username] = user


    def disconnect_wrapper(self, username):
        print "Desconectando usuario: "+username
        del self.client_dictionary[username]
        #self, ip_string, port_string

    def login(self,username,password,ip_string, port_string):
        password = password +"\n"
        print "login: "+username+" "+password
        print "registrados "+str(self.registered_users)
        if self.registered_users.has_key(username) and self.registered_users[username] == password:
            self.connect_wrapper(ip_string,port_string,username)
        else:
            raise Exception(USER_DATA_WRONG)

    def user_to_dictionary(self, username,ip,port):
        user = {}
        user[NAME_CONTACT] = username
        user[IP_CONTACT] = ip
        user[PORT_CONTACT] = port
        #Crea el canal de comunicación
        user[CHANNEL_CONTACT] = RequestChannel(contact_ip = ip, contact_port = port, sender = True)
        return user



# **************************************************
#  Definicion de la funcion principal
#**************************************************
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "l", ["local="])
    except getopt.GetoptError:
        print 'Uso con puertos locales:'
        print '$ python Directory/DirectoryServer.py -l <puerto>'
        print 'Uso entre computadoras dentro de la red'
        print '$ python Directory/DirectoryServer.py '
        sys.exit(2)
    if opts: #Si el usuario mandó alguna bandera
        local = True if '-l' in opts[0] else False
    else:
        local = False
        
    if local:
        general_server = GeneralDirectory(port = args[0])
    else:
        general_server = GeneralDirectory()
    general_server.startServer()


if __name__ == '__main__':
    main(sys.argv[1:])
