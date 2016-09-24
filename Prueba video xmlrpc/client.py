import xmlrpclib
import threading
import multiprocessing as mp
import cv2
from cStringIO import StringIO
from numpy.lib import format

proxy = xmlrpclib.ServerProxy("http://localhost:5000/",allow_none = True)

def toString(data):
    f= StringIO()
    format.write_array(f,data)
    return f.getvalue()

def feed_queue():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            data = xmlrpclib.Binary(toString(frame))
            proxy.my_play_video(data)
    #cap.release()

queue = mp.Queue()

p = threading.Thread(target=feed_queue)
#p.daemon = True

p.start()
