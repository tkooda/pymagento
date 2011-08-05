from __future__ import print_function
import os
import unittest
import pymagento


host = None
username = None
api_key = None


class APITestCase(unittest.TestCase):
    def test_connect(self):
        api = pymagento.Magento(host, username, api_key)
        api.close()

class CategoryTestCase(unittest.TestCase):
    def setUp(self):
        self.api = pymagento.Magento(host, username, api_key)

    def tearDown(self):
        self.api.close()

    def test_create_and_delete(self):
        id = self.api.category.create(1, {
            "is_active": True,
            "include_in_menu": False,
            "available_sort_by": "Name",
            "default_sort_by": "Name",
            "name": "Test",
        })
        self.api.category.delete(id)

    def test_show(self):
        id = self.api.category.create(1, {
            "is_active": True,
            "include_in_menu": False,
            "available_sort_by": "Name",
            "default_sort_by": "Name",
            "name": "Test",
        })
        try:
            category = self.api.category.info(id)
            self.assertEqual(category["name"], "Test")
        finally:
            self.api.category.delete(id)

    def test_update(self):
        id = self.api.category.create(1, {
            "is_active": True,
            "include_in_menu": False,
            "available_sort_by": "Name",
            "default_sort_by": "Name",
            "name": "Test",
        })
        try:
            cat = self.api.category.info(id)
            self.assertEqual(cat["name"], "Test")
            self.api.category.update(id, {
                "name": "Testing",
                "available_sort_by": "Name",
                "default_sort_by": "Name",
                "include_in_menu": False,
            })
            updated_cat = self.api.category.info(id)
            # the name has changed...
            self.assertEqual(updated_cat["name"], "Testing")
            cat.pop("name")
            updated_cat.pop("name")
            cat.pop("updated_at")
            updated_cat.pop("updated_at")
            # but they're otherwise the same
            self.assertEqual(cat, updated_cat)

        finally:
            self.api.category.delete(id)


if __name__ == "__main__":
    username = os.environ.get("MAGENTO_USER")
    api_key = os.environ.get("MAGENTO_KEY")
    host = os.environ.get("MAGENTO_HOST")
    if not username or not api_key or not host:
        raise RuntimeError("You must add MAGENTO_USER, MAGENTO_KEY, and \
            MAGENTO_HOST to your environment variables to run the test suite")

    unittest.main()
