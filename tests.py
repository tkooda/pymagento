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


if __name__ == "__main__":
    username = os.environ.get("MAGENTO_USER")
    api_key = os.environ.get("MAGENTO_KEY")
    host = os.environ.get("MAGENTO_HOST")
    if not username or not api_key or not host:
        raise RuntimeError("You must add MAGENTO_USER, MAGENTO_KEY, and \
            MAGENTO_HOST to your environment variables to run the test suite")

    unittest.main()
