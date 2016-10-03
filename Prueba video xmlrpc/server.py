#! /usr/bin/env python
import xmlrpclib
import cv2
import threading
from numpy.lib import format
from cStringIO import StringIO
from SimpleXMLRPCServer import SimpleXMLRPCServer

def toArray(s):
    f = StringIO(s)
    arr = format.read_array(f)
    return arr

class Video(object):    

    def __init__(self):
        super(Video, self).__init__()
        self.r = False
        self.frame = None
        self.frames = []

    def my_pop_queue(self):
        while True:
            if len(self.frames) > 0:
                print "Mostrando frame actual"
                cv2.imshow('frame',self.frames.pop(0))
                print "MOSTRADO frame actual"
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cv2.destroyAllWindows()

    def my_play_video(self, frame):
        self.frames.append(toArray(frame.data))

server = SimpleXMLRPCServer(("localhost", 5000), allow_none = True)

a = Video()
a.r = True
video_thread = threading.Thread(target = a.my_pop_queue)
video_thread.start()

server.register_function(a.my_play_video,'my_play_video')
print "running"
server.serve_forever()