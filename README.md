# pymagento

Pymagento provides python bindings for the
[Magento](http://www.magentocommerce.com) [Core API](http://www.magentocommerce.com/support/magento_core_api).

# Installation

    pip install pymagento


# Usage

```python
import pymagento
api = pymagento.Magento("hostname", "api_user", "api_key")
category_id = api.category.create(1, {"name": "New Category"})
category_info = api.category.info(category_id)
arbitrary_product = api.product.list()[39]
api.category.assignProduct(arbitrary_product["id"])
```

See [magento.com](http://www.magentocommerce.com/support/magento_core_api) for API documentation.
