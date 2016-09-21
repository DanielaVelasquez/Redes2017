#! /usr/bin/env python
# -*- coding: utf-8 -*-

######################################################
# PURPOSE:Interfaz grafica de un cliente en PyQt4    #
#                                                    #
# Vilchis Dominguez Miguel Alonso                    #
#       <mvilchis@ciencias.unam.mx>                  #
#                                                    #
# Notes: El alumno tiene que implementar los métodos #
#       Listados(Instalar python-qt4, python-pyaudio)#
#      sudo apt-get install jackd qjackctl           #
#                                                    #
# Copyright   16-08-2015                             #
#                                                    #
# Distributed under terms of the MIT license.        #
#################################################### #
import sys
from GUI.LoginGUI import LoginGUI
from Constants.Constants import *
from PyQt4 import QtGui
# **************************************************
#  Definicion de la funcion principal
#**************************************************
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "l", ["local="])
    except getopt.GetoptError:
        print 'Uso con puertos locales:'
        print 'GraphicalUserInterface -l'
        print 'Uso entre computadoras dentro de la red'
        print 'GraphicalUserInterface'
        sys.exit(2)
    if opts: #Si el usuario mandó alguna bandera
        local = True if '-l' in opts[0] else False
    else:
        local = False

    app = QtGui.QApplication(sys.argv)
    if local:
        login = LoginGUI(LOCAL)
    else:
        login = LoginGUI()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
