=====================================
Filtering ``catalog_product`` queries
=====================================

This document is not a substitute for the real `Magento API documentation`__.
Much of this information was taken from `Using Collections in Magento`__ .

.. __: http://www.magentocommerce.com/wiki/doc/webservices-api/api/
.. __: http://www.magentocommerce.com/wiki/5_-_modules_and_development/catalog/using_collections_in_magento

``api.catalog_product.list``
============================

.. py:function:: api.catalog_product.list([filters : dict [, storeView : int]]) -> list of dicts
    Retrieve a product list

    Produce an ``AND`` query by adding multiple items to the filter dict::

        {
            'sku': {'null': 'true'},
            'product_id': {'eq': '3047'},
        }

    Produce an ``OR`` query by passing a list of filter dicts::

        {
            'product_id': [
                {'eq': '3047'},
                {'eq': '2979'},
            ],
        }

    Available filters::

        like
        nlike:

            {'sku': {'like': 'S8MST-E13W-WHT-%'}}

        eq
        neq:

            {'sku': {'neq': ''}}

        notnull
        null:

            {'sku': {'null': 'true'}}

        in
        nin:

            {'sku': {'in': ['S8MST-E13W-WHT-SM', 'S8MST-E13W-WHT-MD']}}

        is
        gt
        lt
        gteq
        moreq
        lteq:

            {'status': {'lteq': '1'}}

        finset (mysql's FIND_IN_SET()):

            ??

        from -> to (uses dates)
        date -> to (converts to date)
        datetime -> to (converts to datetime):

            {'created_at': {'from': '2011-09-13 15:31:21'}}

            # converts comparison value types
            {'created_at': {'from': '10 September 2000',
                    'to': '11 September 2000',
                    'date': 'true'}}

    Example of using ``AND`` and ``OR`` queries together:

    .. code-block:: python

        >>> STORE_ID = 1
        >>> all_prods = api.catalog_product.list({
        ...     'status': {'eq': '1'},
        ...     'sku': [{'neq': ''}, {'notnull': 'true'}],
        ...     'upc': [{'neq': ''}, {'notnull': 'true'}],
        ... }, STORE_ID)


``cataloginventory_stock_item.list``
====================================

.. py:function:: api.cataloginventory_stock_item.list([products : list]) -> list of dicts
    Retrieve stock data by product ids

    Usage::

        api.product_stock.list(['S8MST-E14W-WHT-MD', 'S8MST-E14W-WHT-SM'])
