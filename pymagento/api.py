import xmlrpclib


MAGENTO_API_URI = "/api/xmlrpc/"


class Magento(object):
    class MagentoException(Exception):
        pass

    def __init__(self, host, user, passwd):
        self.proxy = xmlrpclib.ServerProxy("http://%s%s" % (host, MAGENTO_API_URI))
        self.token = self.proxy.login(user, passwd)

    def close(self):
        self.proxy.endSession(self.token)

    def __getattr__(self, subapi):
        # this proxies the Magento API type, e.g., Category, Product,
        # or Sales_Order to _proxy_caller
        return _proxy_caller(self, subapi)

    def _call(self, path, *args):
        return self.proxy.call(self.token, path, args)


class _proxy_caller(object):
    def __init__(self, connection, subapi):
        self.subapi = subapi
        self.connection = connection

    def __getattr__(self, remote_function):
        # this combines the function with the api established before
        # (as self.subapi) into the RPC
        path = "%s.%s" % (self.subapi, remote_function)
        def fn(*args):
            return self.connection._call(path, *args)
        fn.func_name = "Magento.%s" % path
        return fn
