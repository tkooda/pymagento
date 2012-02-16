=========
pymagento
=========

pymagento provides Python bindings for the `Magento
<http://www.magentocommerce.com>`_ `Core API
<http://www.magentocommerce.com/support/magento_core_api>`_.

Installation
============

::

    pip install pymagento


Usage
=====

.. code-block:: python

    import pymagento
    api = pymagento.Magento("hostname", "api_user", "api_key")
    category_id = api.category.create(1, {"name": "New Category"})
    category_info = api.category.info(category_id)
    arbitrary_product = api.product.list()[39]
    api.category.assignProduct(arbitrary_product["id"])

Contents
========

.. toctree::
    :maxdepth: 1

    filtering
    multicall

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

