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
import socket, select
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

        try:
            self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #Conexiones actuales
            self.users = {}

            self.s.bind((TCP_IP, TCP_PORT))
            self.s.listen(500)

            self.funtionWrapper = FunctionWrapperDirectory(self.client_dictionary)
            print ("Directorio de ubicacion activo, mi direccion es:")
            print ("(%s, %s))" %(get_ip_address(), port))
            self.run()
        except Exception as e:
            print "Error: "+str(e)

    def run(self):
        while True:
            conn, addr = self.s.accept()
            print "\n"
            threading.Thread(target = self.run_thread, args = (conn,addr)).start()

    def run_thread(self, conn, addr):
        print "Directory server connected with "+addr[0]+ ":"+str(addr[1])
        connected = True
        while connected:
            try:
                data = conn.recv(BUFFER_SIZE)
                print "Data: "+data
                method, params = get_method(data)
                if method == 'connect_wrapper':
                    self.funtionWrapper.connect_wrapper(params[0],params[1],params[2])
                elif method == 'disconnect_wrapper':
                    self.funtionWrapper.disconnect_wrapper(params[0])
                elif method == 'register':
                    self.funtionWrapper.register(params[0],params[1])
                elif method == 'login':
                    val = self.funtionWrapper.login(params[0],params[1],params[2],params[3])
                elif method == 'sendMessage_wrapper':
                    self.funtionWrapper.sendMessage_wrapper(params[0])
                elif method == 'play_audio_wrapper':
                    self.funtionWrapper.play_audio_wrapper(params[0])
                elif method == 'update_contacts':
                    self.funtionWrapper.update_contacts(params[0])
                elif method == 'get_contacts_wrapper':
                    contacts = self.funtionWrapper.get_contacts_wrapper(params[0])
                    conn.sendall(contacts)
                else:
                    conn.sendall(METHOD_NOT_REGISTERED)
                conn.sendall(val)
            except Exception as e:
                connected = False
            
        conn.close()
        


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
        #self.start_thread()

    def start_thread(self):
        self.update_thread = threading.Thread(target = self.update) 
        self.update_thread.daemon = True
        self.update_thread.start()

    def update(self):
        while True:
            try:
                #print "usuarios conectados: "+str(self.client_dictionary)
                for user in self.client_dictionary:
                    d = self.client_dictionary[user]
                    channel = d[CHANNEL_CONTACT]
                   
                    #print "Contactos conectados "+str(self.client_dictionary)
                    c = self.get_contacts_wrapper(user)
                    try:
                        print "Enviando: "+user
                        channel.send_contacts(c)
                    except Exception as e:
                        print "Error: "+str(e)
                        self.disconnect_wrapper(user)
            except Exception as er:
                print "Error updating"+str(er)
            #print "usuarios registrados: "+str(self.registered_users)+"\n"
            #print "usuarios conectados: "+str(self.client_dictionary)
                
            time.sleep(SLEEP)

    def read_users(self):
        archivo = open(FILE_NAME,'r')
        for line in archivo:
            l = line.split(SEP,2)
            username = l[0]
            password = l[1]
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
        
        #Revisa si existe un usuario con dicho nombre
        if self.client_dictionary.has_key(username):
            #No permite la conexión
            raise Exception(USERNAME_USED)
        else:
            print "Iniciando usuario: "+username
            user = self.user_to_dictionary(username,ip_string,port_string)
            self.client_dictionary[username] = user


    def disconnect_wrapper(self, username):
        print "Desconectando usuario: "+username
        del self.client_dictionary[username]
        #self, ip_string, port_string

    def login(self,username,password,ip_string, port_string):
        password = password +"\n"
        #print "registrados "+str(self.registered_users)
        if self.registered_users.has_key(username) and self.registered_users[username] == password:
            self.connect_wrapper(ip_string,port_string,username)
            return OK
        else:
            return USER_DATA_WRONG

    def user_to_dictionary(self, username,ip,port):
        user = {}
        user[NAME_CONTACT] = username
        user[IP_CONTACT] = ip
        user[PORT_CONTACT] = port
        #Crea el canal de comunicación
        user[CHANNEL_CONTACT] = RequestChannel(contact_ip = ip, contact_port = port, sender = True)

        #user[SOCKET_CONTACT] = self.last_connections

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
    #general_server.startServer()


if __name__ == '__main__':
    main(sys.argv[1:])
