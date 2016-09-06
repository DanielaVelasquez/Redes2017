import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

def is_even(n):
    return n % 2 == 0

def python_logo():
     with open("logo.jpg", "rb") as handle:
         return xmlrpclib.Binary(handle.read())

server = SimpleXMLRPCServer(("localhost", 8001))
print "Listening on port 8001..."
server.register_function(is_even, "is_even")
server.register_function(python_logo, "logo")
server.serve_forever()