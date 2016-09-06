import xmlrpclib

proxy = xmlrpclib.ServerProxy("http://localhost:8001/")
print "3 is even: %s" % str(proxy.is_even(3))
print "100 is even: %s" % str(proxy.is_even(100))
with open("fetched_presidencia_logo.jpg", "wb") as handle:
    handle.write(proxy.logo().data)