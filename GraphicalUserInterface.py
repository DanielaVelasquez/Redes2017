#! /usr/bin/env python
# -*- coding: utf-8 -*-

######################################################
# PURPOSE:Interfaz grafica de un cliente en PyQt4    #
#                                                    #
# Vilchis Dominguez Miguel Alonso                    #
#       <mvilchis@ciencias.unam.mx>                  #
#                                                    #
# Notes: El alumno tiene que implementar la parte    #
#       comentada como TODO(Instalar python-qt)      #
#                                                    #
# Copyright   16-08-2015                             #
#                                                    #
# Distributed under terms of the MIT license.        #
#################################################### #
import sys, getopt
from Constants.Constants import *
from GUI.LoginGUI import LoginGUI
from PyQt4 import QtGui
# **************************************************
#  Definicion de la funcion principal
#**************************************************
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "l", ["local="])
    except getopt.GetoptError:
        raise Exception(WRONG_OPTION)
    #Si el usuario mandó alguna bandera
    if opts: 
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