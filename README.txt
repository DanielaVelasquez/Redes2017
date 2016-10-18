Integrantes:    
	Angie Daniela Velásquez Garzón  
	Bernal Cedillo Enrique Antonio  

Version python: 2.7.12  
Version pyaudio 0.2.9  
Version numpy 1.6.1  

-) Construcción de la imagen:  

	Imágen de servidor:  
		docker build -t imagen_servidor .

	Imágen de cliente:  
		docker build -t imagen_cliente .

-) Ejecución:  

	xhost +local:root

	Contenedor de servidor:
		docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY --privileged imagen_servidor

	Contenedor de cliente:
		docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY --privileged imagen_cliente

Borrado de imagen:
	docker rmi <REPOSITORY>

Borrado de TODOS los contenedores:
	docker rm $(docker ps -aq)
