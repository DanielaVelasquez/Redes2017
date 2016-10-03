#!/bin/sh
FROM ubuntu:14.04

#Instalamos firefox
RUN apt-get update && apt-get install -y firefox

# Idealmente tambien esto, para las practicas de python
#sudo apt-get install python-pyaudio
#sudo apt-get install python-qt4
#sudo apt-get install python-numpy
#sudo apt-get install python-opencv

#Reemplazamos 1000 con el usuario / y id del grupo
# No se que es esto
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/developer && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown ${uid}:${gid} -R /home/developer

# Falta agregar lista de devices (microfono y camara)

#Cambio de usuario
USER developer
#Variable de entorno HOME
ENV HOME /home/developer

#Comando a usar
# Deberia abrirse una terminal con python, pero ni idea como
CMD /usr/bin/firefox
