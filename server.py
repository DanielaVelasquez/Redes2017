#! /usr/bin/env pythonb

import xmlrpclib
import pickle
import cv2
import threading

from SimpleXMLRPCServer import SimpleXMLRPCServer


class Video(object):
	
	def __init__(self):
		super(Video, self).__init__()
		self.r = False
		self.frame = None
		


	def reproduce(self):
		print "Iniciando hilo"
		while self.r:
			#print "Mostrando"
			cv2.imshow('frame',self.frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		cv2.destroyAllWindows()

	def reproduce_video(self, video):

		print "reproducing..."

		self.frame = pickle.loads(video)

		if not self.r:
			print "no estaba reproduciendo"
			self.r = True
			print "Lanzando hilo"
			p = threading.Thread(target=self.reproduce)
			p.start()
			print "lanzado"



	#cap.release()



server = SimpleXMLRPCServer(("localhost", 5000), allow_none = True)

a = Video()

server.register_function(a.reproduce_video,'reproduce_video')

print "running"

server.serve_forever()

