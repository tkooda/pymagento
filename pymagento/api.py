import xmlrpclib as xmlrpc


MAGENTO_API_URI = "/api/xmlrpc/"


class Magento(object):
    class MagentoException(Exception):
        pass

    def __init__(self, host, user, passwd):
        self.proxy = xmlrpc.ServerProxy("http://%s%s" % (host, MAGENTO_API_URI))
        self.token = self.proxy.login(user, passwd)

    def close(self):
        self.proxy.endSession(self.token)

    def __getattr__(self, subapi):
        return _proxy_caller(self, subapi)

    def _call(self, path, *args):
        return self.proxy.call(self.token, path, args)

class _proxy_caller(object):
    def __init__(self, connection, subapi):
        self.subapi = subapi
        self.connection = connection

    def __getattr__(self, remote_function):
        path = "%s.%s" % (self.subapi, remote_function)
        def fn(*args):
            return self.connection._call(path, *args)
        fn.func_name = "Magento.%s" % path
        return fn
