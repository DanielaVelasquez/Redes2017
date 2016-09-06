import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

def is_even(n):
    return n % 2 == 0

def python_logo():
     with open("logo.jpg", "rb") as handle:
         return xmlrpclib.Binary(handle.read())

server = SimpleXMLRPCServer(("192.168.1.83", 5000),allow_none=True)
print "Listening on port 5000..."
server.register_function(is_even, "is_even")
server.register_function(python_logo, "logo")
server.serve_forever()