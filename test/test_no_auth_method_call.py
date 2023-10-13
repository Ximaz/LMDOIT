import sys
import unittest

sys.path.append("../")
from lmdoit import *


class TestNoneParameters(unittest.TestCase):
    def test_url_none(self):
        lmdoit_api = LMDOIT()

        try:
            auth = lmdoit_api.no_auth(url=None, method="POST")
        except ValueError as e:
            self.assertEqual(str(e), "You must supply both 'url' and 'method' parameters.")

    def test_method_none(self):
        lmdoit_api = LMDOIT()

        try:
            auth = lmdoit_api.no_auth(url="https://www.site.com", method=None)
        except ValueError as e:
            self.assertEqual(str(e), "You must supply both 'url' and 'method' parameters.")

    def test_both_none(self):
        lmdoit_api = LMDOIT()

        try:
            auth = lmdoit_api.no_auth(url=None, method=None)
        except ValueError as e:
            self.assertEqual(str(e), "You must supply both 'url' and 'method' parameters.")

    def test_both_ok(self):
        lmdoit_api = LMDOIT()

        auth = lmdoit_api.no_auth(url="https://www.site.com", method="POST")
        self.assertIsInstance(auth, LMDOIT_Request_Process)

if __name__ == "__main__":
    unittest.main()
