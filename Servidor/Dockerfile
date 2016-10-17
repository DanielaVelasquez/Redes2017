#!/bin/sh
# Imagen de linux a utilizar
FROM ubuntu:latest

# Instalamos dependencias necesarias
RUN	apt-get update && \
	apt-get install -y --no-install-recommends python-pyaudio && \
    apt-get install -y --no-install-recommends python-qt4 && \
    apt-get install -y --no-install-recommends python-numpy

# Creamos el directorio de trabajo
RUN mkdir Redes-17

# Agregamos los archivos que se encuentren en la carpeta del Dockerfile
ADD . Redes-17

# Nombramos el directorio creado como directorio de trabajo
WORKDIR Redes-17

#Comando a usar
CMD cd Directory && python DirectoryServer.py -l 5000