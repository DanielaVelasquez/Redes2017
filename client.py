import xmlrpclib

proxy = xmlrpclib.ServerProxy("http://192.168.1.83:5000/",allow_none=True)
a = proxy.is_even(3)
print "rta: "+str(a)