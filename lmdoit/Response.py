import pathlib
import re
import typing
import urllib.error

import bs4
import requests


OnErrorCallback = typing.Callable[[requests.Session, requests.Response, urllib.error.HTTPError | requests.exceptions.HTTPError], typing.Any]


class LMDOIT_Response:
    def __init__(self, session: requests.Session, response: requests.Response) -> None:
        self._session = session
        self._response = response

        self._soup = bs4.BeautifulSoup(
            markup=self._response.text, features="html.parser"
        )

    def save_response_for_debug(self, output_dest: str | pathlib.Path):
        if isinstance(output_dest, str):
            output_dest = pathlib.Path(output_dest)
        
        if not isinstance(output_dest, pathlib.Path):
            raise ValueError("Invalid type for 'output_dest'.")
        
        with open(file=output_dest.absolute(), mode="wb+") as stream:
            stream.write(self._response.content)

        return self

    def find_html_element(
        self, css_selector: str, return_all_found: bool = False
    ) -> bs4.ResultSet[bs4.Tag] | bs4.Tag | None:
        if not isinstance(css_selector, str):
            raise ValueError("Invalid type for 'css_selector'.")

        if not isinstance(return_all_found, bool):
            raise ValueError("Invalid type for 'return_all_found'.")

        return (
            self._soup.select(selector=css_selector)
            if not return_all_found
            else self._soup.select_one(selector=css_selector)
        )

    def match_regex(self, regex: str | re.Pattern, match_each_line: bool = True) -> list:
        if isinstance(regex, str):
            regex = re.compile(pattern=regex, flags=re.MULTILINE if match_each_line else 0)

        if not isinstance(regex, re.Pattern):
            raise ValueError("Invalid type for 'regex'.")

        return regex.findall(string=self._response.text)

    def to_json(self):
        return self._response.json()

    def handle_error(self, on_error_callback: OnErrorCallback):
        if not isinstance(on_error_callback, typing.Callable):
            raise ValueError("Invalid type for 'on_error_callback'.")

        try:
            self._response.raise_for_status()
        except (urllib.error.HTTPError, requests.exceptions.HTTPError) as traceback:
            on_error_callback(self._session, self._response, traceback)
        return self
