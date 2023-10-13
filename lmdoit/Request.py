import requests

from .Response import LMDOIT_Response


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
