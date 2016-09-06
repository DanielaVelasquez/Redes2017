import xmlrpclib

proxy = xmlrpclib.ServerProxy("http://192.168.1.83:8001/",allow_none=True)
proxy.is_even(3)