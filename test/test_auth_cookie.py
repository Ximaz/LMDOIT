import sys
import unittest

import requests.cookies

sys.path.append("../")
from lmdoit import *


class TestCookieString(unittest.TestCase):
    def test_str(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")

        first_cookie = "username=bob; login_date=20230810_135603"
        auth.cookie(cookie=first_cookie)

        second_cookie = "last_post_id=918829937; last_message_id=99288839"
        auth.cookie(cookie=second_cookie)

        self.assertDictEqual(
            auth._session.cookies.get_dict(),
            {
                "username": "bob",
                "login_date": "20230810_135603",
                "last_post_id": "918829937",
                "last_message_id": "99288839",
            },
        )


class TestCookieDict(unittest.TestCase):
    def test_dict(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")

        first_cookie = {"username": "bob", "login_date": "20230810_135603"}
        auth.cookie(cookie=first_cookie)

        second_cookie = {"last_post_id": "918829937", "last_message_id": "99288839"}
        auth.cookie(cookie=second_cookie)

        self.assertDictEqual(
            auth._session.cookies.get_dict(),
            {
                "username": "bob",
                "login_date": "20230810_135603",
                "last_post_id": "918829937",
                "last_message_id": "99288839",
            },
        )


class TestCookieJar(unittest.TestCase):
    def test_requests_cookie_jar(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")

        first_cookie = requests.cookies.RequestsCookieJar()
        first_cookie.set_cookie(requests.cookies.create_cookie("username", "bob"))
        first_cookie.set_cookie(
            requests.cookies.create_cookie("login_date", "20230810_135603")
        )
        auth.cookie(cookie=first_cookie)

        second_cookie = requests.cookies.RequestsCookieJar()
        second_cookie.set_cookie(
            requests.cookies.create_cookie("last_post_id", "918829937")
        )
        second_cookie.set_cookie(
            requests.cookies.create_cookie("last_message_id", "99288839")
        )
        auth.cookie(cookie=second_cookie)

        self.assertDictEqual(
            auth._session.cookies.get_dict(),
            {
                "username": "bob",
                "login_date": "20230810_135603",
                "last_post_id": "918829937",
                "last_message_id": "99288839",
            },
        )


class TestCookieMixed(unittest.TestCase):
    def test_mixed(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")

        first_cookie = "username=bob; login_date=20230810_135603"
        auth.cookie(cookie=first_cookie)

        second_cookie = {"last_post_id": "918829937", "last_message_id": "99288839"}
        auth.cookie(cookie=second_cookie)

        third_cookie = requests.cookies.RequestsCookieJar()
        third_cookie.set_cookie(requests.cookies.create_cookie("expires_at", "3600"))
        third_cookie.set_cookie(requests.cookies.create_cookie("auth_method", "basic"))
        auth.cookie(cookie=third_cookie)

        self.assertDictEqual(
            auth._session.cookies.get_dict(),
            {
                "username": "bob",
                "login_date": "20230810_135603",
                "last_post_id": "918829937",
                "last_message_id": "99288839",
                "expires_at": "3600",
                "auth_method": "basic",
            },
        )


if __name__ == "__main__":
    unittest.main()
