import requests
import requests.cookies

from .Auth import LMDOIT_Auth_Process
from .Request import LMDOIT_Request_Process


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
        :rtype: :class:`LMDOIT_Auth_Process`

        :Example:
        >>> auth(
        >>>     url="https://www.example.com/auth",
        >>>     method="POST"
        >>> ).cookie("username=bob; age=18")
        """
        if any([p is None for p in [url, method]]):
            raise ValueError("You must supply both 'url' and 'method' parameters.")

        return LMDOIT_Auth_Process(session=self._session, url=url, method=method)

    def no_auth(self, url: str, method: str) -> LMDOIT_Request_Process:
        """
        Prepare the request of the client without authentication process using
        the provided url and method.

        :param url: The URL to which the auth process happens.
        :param method: The request method to use ("GET", "POST", ...).
        :type url: str
        :type method: str
        :return: A new LMDOIT Request Process
        :rtype: :class:`LMDOIT_Request_Process`

        :Example:
        >>> no_auth(
        >>>     url="https://www.example.com/free_api/endpoint",
        >>>     method="POST"
        >>> )
        """
        if any([p is None for p in [url, method]]):
            raise ValueError("You must supply both 'url' and 'method' parameters.")

        return LMDOIT_Request_Process(session=self._session, url=url, method=method)
