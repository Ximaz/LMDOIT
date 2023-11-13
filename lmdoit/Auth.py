import requests
import requests.cookies

from .Request import LMDOIT_Request_Process


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

        if additionnal_cookies is None:
            raise ValueError("Unable to parse 'cookie'.")

        return {**current_dict_jar, **additionnal_cookies}

    def cookie(
        self, cookie: str | dict | requests.cookies.RequestsCookieJar
    ) -> LMDOIT_Request_Process:
        """
        The cookie authentication method will be used.

        :param cookie: The cookie to place in headers for future requests
        :type cookie: str | dict | requests.cookie.RequestsCookieJar
        :return: A new LMDOIT Request Process
        :rtype: :class:`LMDOIT_Request_Process`
        """
        self._session.cookies = requests.cookies.cookiejar_from_dict(
            cookie_dict=self._parse_cookie(cookie=cookie)
        )

        return LMDOIT_Request_Process(
            session=self._session, url=self._url, method=self._method
        )
