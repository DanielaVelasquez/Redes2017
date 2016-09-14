import xmlrpclib
import pickle
import threading
import multiprocessing as mp
import cv2



def feed_queue(q):

	cap = cv2.VideoCapture(0)
	while True:

		ret, frame = cap.read()
		if ret:
			q.put(pickle.dumps(frame))



proxy = xmlrpclib.ServerProxy("http://localhost:5000/",allow_none = True)



queue = mp.Queue()

p = threading.Thread(target=feed_queue, args=(queue,))

p.start()



while True:

	d = queue.get()

	proxy.reproduce_video(d)