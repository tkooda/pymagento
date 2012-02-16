==============================
Magento's ``multiCall`` method
==============================

Magento's ``multiCall`` method (not to be confused with the ``xmlrpclib``
function of the same name) allows multiple API methods to be called in one
request which can drastically speed up multiple queries.

The ``multiCall`` wrapper breaks from the normal ``pymagento`` usage to make it
easier to programatically generate bulk queries. For example:

.. code-block:: python

    >>> all_prods = api.catalog_product.list({
    ...     'sku': [{'neq': ''}, {'notnull': 'true'}],
    ... })
    >>> len(all_prods)
    200
    >>> all_skus = [i['sku'] for i in all_prods]
    >>> all_prod_details = api.multiCall([
    ...     [['catalog_product.info', [sku]] for sku in all_skus],
    ...     [['catalog_product_attribute_media.list', [sku]] for sku in all_skus],
    ... ])

.. note:: ``multiCall`` does not raise faultCode exceptions

    With normal ``pymagento`` use, if you call a server method incorrectly (by
    calling a method that does not exist or calling a method with incorrect
    parameters) ``xmlrpclib`` will raise a ``Fault`` exception:

    .. code-block:: python

        >>> api.thisdoesnotexist.info()
        Traceback (most recent call last):
            ...
        Fault: <Fault 3: 'Invalid api path.'>

    When using Magento's ``multiCall`` method those ``Fault`` codes are embeded
    in the return data structure so you will have to look for them manually:

    .. code-block:: python

        >>> api.multiCall([['thisdoesnotexist', []]])
        [{'faultCode': '3', 'faultMessage': 'Invalid api path.', 'isFault': True}]
