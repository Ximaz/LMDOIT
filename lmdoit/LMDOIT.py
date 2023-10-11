import requests
import requests.cookies


class LMDOIT_Auth_Process:
    """
    The LMDOIT Auth Process Interface

    This class will manage the authentication process.
    """

    def __init__(
        self, session: requests.Session, url: str, method: str, headers: dict = None
    ) -> None:
        self._session = session
        self._session.headers = {**self._session.headers, **(headers or {})}

        self._url = url
        self._method = method

    def cookie(self, cookie: str | dict | requests.cookies.RequestsCookieJar):
        if not isinstance(cookie, (str, dict, requests.cookies.RequestsCookieJar)):
            raise ValueError("Invalid type for 'cookie'.")

        additionnal_cookies = None
        current_jar = self._session.cookies.get_dict()

        if isinstance(cookie, requests.cookies.RequestsCookieJar):
            additionnal_cookies = cookie.get_dict()

        if isinstance(cookie, str):
            additionnal_cookies = dict([c.split("=", 1) for c in cookie.split("; ")])

        if isinstance(cookie, dict) and additionnal_cookies is None:
            additionnal_cookies = cookie

        new_jar = {**current_jar, **additionnal_cookies}

        self._session.cookies = requests.cookies.cookiejar_from_dict(
            cookie_dict=new_jar
        )

        return self


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

    def auth(self, url: str, method: str, headers: dict = None) -> LMDOIT_Auth_Process:
        """
        Prepare the authentication of the client using the provided url and
        method.

        :param url: The URL to which the auth process happens.
        :param method: The request method to use ("GET", "POST", ...).
        :param headers: (optionnal) dict representing custom headers.
        :type url: str
        :type method: str
        :type headers: dict
        :return: A new LMDOIT Auth Process
        :rtype: LMDOIT_Auth_Process

        :Example:
        >>> auth(
        >>>     url="https://www.example.com/auth",
        >>>     method="POST",
        >>>     headers={
        >>>         "Referer": "https://www.example.com/"
        >>>     }
        >>> )
        """
        if any([p is None for p in [url, method]]):
            raise ValueError("You must supply both 'url' and 'method' parameters.")

        return LMDOIT_Auth_Process(
            session=self._session, url=url, method=method, headers=headers
        )
