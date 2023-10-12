import sys
import unittest


sys.path.append("../")
from lmdoit import LMDOIT


class TestSetURLParamsFromDict(unittest.TestCase):
    def test_good_format(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")
        req = auth.cookie(cookie="username=bob; login_date=20230810_135603")
        req.set_url_params(
            params={
                "username": "bob",
                "hashed_password": True,
                "action": 3,
                "salt": 4992.004,
            }
        )
        self.assertDictEqual(
            dict(req)["params"],
            {"username": "bob", "hashed_password": True, "action": 3, "salt": 4992.004},
        )

    def test_empty_dict(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")
        req = auth.cookie(cookie="username=bob; login_date=20230810_135603")
        req.set_url_params(params={})
        self.assertDictEqual(
            dict(req)["params"],
            {},
        )


class TestSetHeadersFromKV(unittest.TestCase):
    def test_good_format(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")
        req = auth.cookie(cookie="username=bob; login_date=20230810_135603")
        req.set_url_param(key="username", value="bob")
        req.set_url_param(key="hashed_password", value=True)
        req.set_url_param(key="action", value=3)
        req.set_url_param(key="salt", value=4992.004)

        req.set_custom_header(key="X-Requested-With", value="XMLHttpRequest")
        self.assertDictEqual(
            dict(req)["params"],
            {"username": "bob", "hashed_password": True, "action": 3, "salt": 4992.004},
        )


if __name__ == "__main__":
    unittest.main()
