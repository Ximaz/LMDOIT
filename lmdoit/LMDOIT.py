import requests
import requests.cookies


class LMDOIT_Response:
    def __init__(self, session: requests.Session, response: requests.Response) -> None:
        self._session = session
        self._response = response


class LMDOIT_Request_Process:
    def __init__(self, session: requests.Session, url: str, method: str) -> None:
        self._session = session
        self._url = url
        self._method = method

        self._params = {}
        self._custom_headers = {}

    def set_url_param(self, key: str, value: str | int | bool | float):
        if not isinstance(key, str):
            raise ValueError("Invalid type for 'key'.")

        if not isinstance(value, (str, int, bool, float)):
            raise ValueError("Invalid type for 'value'.")

        self._params[key.strip()] = value
        return self

    def set_url_params(self, params: str | bytes | dict):
        if not isinstance(params, (str, bytes, dict)):
            raise ValueError("Invalid type for 'params'.")

        if isinstance(params, bytes):
            params = params.decode("utf-8")

        if isinstance(params, str):
            params = dict([v.split("=", 1) for v in params.split("&")])

        for k, v in params.items():
            self.set_url_param(key=k, value=v)

        return self

    def set_custom_header(self, key: str, value: str | int | bool | float):
        if not isinstance(key, str):
            raise ValueError("Invalid type for 'key'.")

        if not isinstance(value, (str, int, bool, float)):
            raise ValueError("Invalid type for 'value'.")

        self._custom_headers[key.strip()] = value
        return self

    def set_custom_headers(self, headers: dict):
        if not isinstance(headers, dict):
            raise ValueError("Invalid type for 'headers'.")

        for k, v in headers.items():
            self.set_custom_header(key=k, value=v)

        return self

    def set_custom_headers_from_raw(self, raw_headers: str):
        if not isinstance(raw_headers, str):
            raise ValueError("Invalid type for 'raw_headers'.")

        headers = dict(
            [
                l.split(": ", 1)
                for l in map(str.strip, raw_headers.strip().splitlines())
                if len(l) > 0 and not l.startswith(":")
            ]
        )
        self.set_custom_headers(headers=headers)
        return self

    def __iter__(self):
        for k, v in {
            "custom_headers": self._custom_headers,
            "method": self._method,
            "params": self._params,
            "session": self._session,
            "url": self._url,
        }.items():
            yield (k, v)

    def get_response(self) -> LMDOIT_Response:
        response = self._session.request(
            method=self._method,
            url=self._url,
            params=self._params,
            headers=self._custom_headers,
        )
        return LMDOIT_Response(session=self._session, response=response)


class LMDOIT_Auth_Process:
    """
    The LMDOIT Auth Process Interface

    This class will manage the authentication process.
    """

    def __init__(self, session: requests.Session, url: str, method: str) -> None:
        self._session = session

        self._url = url
        self._method = method

    def _parse_cookie(
        self, cookie: str | dict | requests.cookies.RequestsCookieJar
    ) -> dict:
        if not isinstance(cookie, (str, dict, requests.cookies.RequestsCookieJar)):
            raise ValueError("Invalid type for 'cookie'.")

        additionnal_cookies = None
        current_dict_jar = self._session.cookies.get_dict()

        if isinstance(cookie, requests.cookies.RequestsCookieJar):
            additionnal_cookies = cookie.get_dict()

        if isinstance(cookie, str):
            additionnal_cookies = dict([c.split("=", 1) for c in cookie.split("; ")])

        if isinstance(cookie, dict) and additionnal_cookies is None:
            additionnal_cookies = cookie

        return {**current_dict_jar, **additionnal_cookies}

    def cookie(
        self, cookie: str | dict | requests.cookies.RequestsCookieJar
    ) -> LMDOIT_Request_Process:
        """
        The cookie authentication method will be used.

        :param cookie: The cookie to place in headers for future requests
        :type cookie: str | dict | requests.cookie.RequestsCookieJar
        :return: A new LMDOIT Request Process
        :rtype: LMDOIT_Request_Process
        """
        self._session.cookies = requests.cookies.cookiejar_from_dict(
            cookie_dict=self._parse_cookie(cookie=cookie)
        )

        return LMDOIT_Request_Process(
            session=self._session, url=self._url, method=self._method
        )


class LMDOIT:
    """
    The LMDOIT Interface

    This class will manage all requests process for you :
    -   authenticating,
    -   metadata gathering,
    -   downloading,
    -   ...
    """

    def __init__(self) -> None:
        self._session = requests.Session()

    def auth(self, url: str, method: str) -> LMDOIT_Auth_Process:
        """
        Prepare the authentication of the client using the provided url and
        method.

        :param url: The URL to which the auth process happens.
        :param method: The request method to use ("GET", "POST", ...).
        :type url: str
        :type method: str
        :return: A new LMDOIT Auth Process
        :rtype: LMDOIT_Auth_Process

        :Example:
        >>> auth(
        >>>     url="https://www.example.com/auth",
        >>>     method="POST"
        >>> )
        """
        if any([p is None for p in [url, method]]):
            raise ValueError("You must supply both 'url' and 'method' parameters.")

        return LMDOIT_Auth_Process(session=self._session, url=url, method=method)
