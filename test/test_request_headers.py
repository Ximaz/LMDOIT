import sys
import unittest


sys.path.append("../")
from lmdoit import LMDOIT


EXPECTED = {
    "Accept": "text/html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "fr-FR,fr;q=0.9",
    "Connection": "keep-alive",
    "Host": "github.com",
    "Referer": "https://github.com/USER/REPOSITORY",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "X-Requested-With": "XMLHttpRequest",
}


class TestRawHeaders(unittest.TestCase):
    def test_good_format(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")
        req = auth.cookie(cookie="username=bob; login_date=20230810_135603")
        req.set_custom_headers_from_raw(
            raw_headers="""
:method: GET
:scheme: https
:authority: github.com
Accept: text/html
Accept-Encoding: gzip, deflate, br
Accept-Language: fr-FR,fr;q=0.9
Connection: keep-alive
Host: github.com
Referer: https://github.com/USER/REPOSITORY
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15
X-Requested-With: XMLHttpRequest
"""
        )
        self.assertDictEqual(
            dict(req)["custom_headers"],
            EXPECTED,
        )

    def test_empty(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")
        req = auth.cookie(cookie="username=bob; login_date=20230810_135603")
        req.set_custom_headers_from_raw(raw_headers="")
        self.assertDictEqual(
            dict(req)["custom_headers"],
            {},
        )

    def test_dangling_format(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")
        req = auth.cookie(cookie="username=bob; login_date=20230810_135603")
        req.set_custom_headers_from_raw(
            raw_headers="""
:method: GET
:scheme: https
:authority: github.com

                                        
Accept: text/html
    Accept-Encoding: gzip, deflate, br
Accept-Language: fr-FR,fr;q=0.9
Connection: keep-alive
        Host: github.com
Referer: https://github.com/USER/REPOSITORY
Sec-Fetch-Dest: empty

                                        Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15
X-Requested-With: XMLHttpRequest
"""
        )
        self.assertDictEqual(
            dict(req)["custom_headers"],
            EXPECTED,
        )


class TestSetHeadersFromDict(unittest.TestCase):
    def test_good_format(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")
        req = auth.cookie(cookie="username=bob; login_date=20230810_135603")
        req.set_custom_headers(headers=EXPECTED)
        self.assertDictEqual(
            dict(req)["custom_headers"],
            EXPECTED,
        )

    def test_empty_dict(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")
        req = auth.cookie(cookie="username=bob; login_date=20230810_135603")
        req.set_custom_headers(headers={})
        self.assertDictEqual(
            dict(req)["custom_headers"],
            {},
        )

    def test_non_str_values(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")
        req = auth.cookie(cookie="username=bob; login_date=20230810_135603")
        req.set_custom_headers(
            headers={
                "X-Is-Connected": True,
                "X-Age-Verification": 13,
                "X-Username": "Ximaz",
                "X-Custom-Pi": 3.1415,
            }
        )
        self.assertDictEqual(
            dict(req)["custom_headers"],
            {
                "X-Is-Connected": True,
                "X-Age-Verification": 13,
                "X-Username": "Ximaz",
                "X-Custom-Pi": 3.1415,
            },
        )


class TestSetHeadersFromKV(unittest.TestCase):
    def test_good_format(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")
        req = auth.cookie(cookie="username=bob; login_date=20230810_135603")
        req.set_custom_header(key="Accept", value="text/html")
        req.set_custom_header(key="Accept-Encoding", value="gzip, deflate, br")
        req.set_custom_header(key="Accept-Language", value="fr-FR,fr;q=0.9")
        req.set_custom_header(key="Connection", value="keep-alive")
        req.set_custom_header(key="Host", value="github.com")
        req.set_custom_header(key="Referer", value="https://github.com/USER/REPOSITORY")
        req.set_custom_header(key="Sec-Fetch-Dest", value="empty")
        req.set_custom_header(key="Sec-Fetch-Mode", value="cors")
        req.set_custom_header(key="Sec-Fetch-Site", value="same-origin")
        req.set_custom_header(key="User-Agent", value="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15")
        req.set_custom_header(key="X-Requested-With", value="XMLHttpRequest")
        self.assertDictEqual(
            dict(req)["custom_headers"],
            EXPECTED,
        )

    def test_non_str_values(self):
        lmdoit_api = LMDOIT()
        auth = lmdoit_api.auth(url="https://www.site.com", method="POST")
        req = auth.cookie(cookie="username=bob; login_date=20230810_135603")
        req.set_custom_header(key="X-Is-Connected", value=True)
        req.set_custom_header(key="X-Age-Verification", value=13)
        req.set_custom_header(key="X-Username", value="Ximaz")
        req.set_custom_header(key="X-Custom-Pi", value=3.1415)
        self.assertDictEqual(
            dict(req)["custom_headers"],
            {
                "X-Is-Connected": True,
                "X-Age-Verification": 13,
                "X-Username": "Ximaz",
                "X-Custom-Pi": 3.1415,
            },
        )


if __name__ == "__main__":
    unittest.main()
