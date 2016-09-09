import xmlrpclib

MAGENTO_API_URI = "/api/xmlrpc/"

class Magento(object):
    """A small wrapper around Magento's xmlrpc implementation

    Usage::

        import pymagento
        api = pymagento.Magento('myhost', 'myuser', 'mypass')
        api.catalog_product.info('S8MST-E12W-WHT-MD')

    Roughly equivalent to:

    >>> import xmlrpclib
    >>> server = xmlrpclib.ServerProxy('http://{0}{1}'.format(host, MAGENTO_API_URI))
    >>> session = server.login(user, passwd)
    >>> server.call(session, 'catalog_product.info', ['S2BLCZ-013'])
    {...}

    Query what methods are available on the server via:

    >>> server.system.listMethods()
    [...]

    """
    class MagentoException(Exception):
        pass

    def __init__(self, host, user, passwd, scheme="http"):
        self.proxy = xmlrpclib.ServerProxy("%s://%s%s" % (scheme,host, MAGENTO_API_URI))
        self.token = self.proxy.login(user, passwd)

    def close(self):
        self.proxy.endSession(self.token)

    def __getattr__(self, subapi):
        # this proxies the Magento API type, e.g., Category, Product,
        # or Sales_Order to _proxy_caller
        return _proxy_caller(self, subapi)

    def _call(self, path, *args):
        """A wrapper for Magento's ``call`` method

        >>> server.system.methodSignature('call')
        [...]

        """
        return self.proxy.call(self.token, path, args)

    def multiCall(self, calls):
        """Takes a list of lists containing the API call and the args

        Usage::

            api.multiCall([
                ['catalog_product.info', ['S2BLCZ-013']],
                ['catalog_product.info', ['S2INCZ-052']],
            ])

        multiCall (afaik) doesn't raise faultCode exceptions so you need to
        look for 'isFault' in the return keys:

        >>> server.multiCall(session, [['fakecall', []]])
        [{'faultCode': '3', 'faultMessage': 'Invalid api path.', 'isFault': True}]

        Equivalent to:

        >>> server.system.methodSignature('multiCall')
        [...]
        >>> server.multiCall(session, [
        ...     ['catalog_product.info', ['S2BLCZ-013']],
        ...     ['catalog_product.info', ['S2INCZ-052']],
        ... ])
        [{...}, {...}]

        """
        return self.proxy.multiCall(self.token, calls)

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
