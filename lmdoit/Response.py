from __future__ import annotations  # Fix the circular import.

import json
import pathlib
import re
import typing
import urllib.error

import bs4
import requests

from . import Request

OnErrorCallback = typing.Callable[
    [
        requests.Session,
        requests.Response,
        urllib.error.HTTPError | requests.exceptions.HTTPError,
    ],
    typing.Any,
]

_JSON_REGEX = re.compile(
    r"(?:[{\[]{1}(?:[,:{}\[\]0-9.\-+Eaeflnr-u \n\r\t]|\".*?\")+[}\]]{1})",
    flags=re.MULTILINE,
)


class LMDOIT_Response:
    def __init__(self, session: requests.Session, response: requests.Response) -> None:
        self._session = session
        self._response = response

        self._soup = bs4.BeautifulSoup(
            markup=self._response.text, features="html.parser"
        )

    def save_response_for_debug(self, output_dest: str | pathlib.Path):
        """
        Save the text response into a file at `output_dest`. It's recommanded
        while you're still developing your solution in order to check what the
        server exactly responded and try to debug the response correctly.

        :param output_dest: The output destination of the file.
        :type output_dest: `str` | `pathlib.Path`
        """

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
        """
        Return all found elements according to `css_selector` which represents
        the selector to use, and the `return_all_found` value which determine
        whether or not return one or all results.

        :param css_selector: The CSS selector to match.
        :param return_all_found: (optionnal) Returns one or more elements.
        :type css_selector: `str`
        :type return_all_found: `bool`
        :return: An tag list, just one tag, or None if none was found.
        :rtype: `bs4.ResultSet[bs4.Tag]` | `bs4.Tag` | `None`
        """

        if not isinstance(css_selector, str):
            raise ValueError("Invalid type for 'css_selector'.")

        if not isinstance(return_all_found, bool):
            raise ValueError("Invalid type for 'return_all_found'.")

        return (
            self._soup.select(selector=css_selector)
            if not return_all_found
            else self._soup.select_one(selector=css_selector)
        )

    def find_all_scripts_element(self) -> list[bs4.Tag]:
        """
        Find all both loaded and static scripts elements each as a new
        :class:`bs4.Tag`.

        :return: The list of found scripts.
        :rtype:  `list[bs4.Tag]`
        """
        return self._soup.select(selector="script")

    def find_static_scripts_elements(self) -> list[bs4.Tag]:
        """
        Find all static scripts elements each as :class:`bs4.Tag`.

        :return: The list of found scripts.
        :rtype:  `list[bs4.Tag]`
        """
        return list(
            filter(lambda s: not s.has_attr("src"), self.find_all_scripts_element())
        )

    def find_loaded_scripts_elements(self) -> list[bs4.Tag]:
        """
        Find all loaded scripts elements each as a new :class:`bs4.Tag`.

        :return: The list of found scripts.
        :rtype:  `list[bs4.Tag]`
        """
        return list(
            filter(lambda s: s.has_attr("src"), self.find_all_scripts_element())
        )

    def find_loaded_scripts_as_preload(self) -> list[Request.LMDOIT_Request_Process]:
        """
        Find all loaded scripts elements each as a new :class:`LMDOIT_Request_Process`.

        :return: The list of found scripts.
        :rtype:  `list[LMDOIT_Request_Process]`
        """

        return [
            Request.LMDOIT_Request_Process(session=self._session, url=src, method="GET")
            for src in map(
                lambda s: s.get("src", None), self.find_loaded_scripts_elements()
            )
            if isinstance(src, str)
        ]

    def _is_valid_json(self, o, /) -> bool:
        try:
            json.loads(o)
        except json.decoder.JSONDecodeError:
            return False
        return True

    def find_json_objects_from_scripts_element(
        self, application_json_only: bool = False
    ) -> typing.Generator[typing.Any, typing.Any, typing.Any]:
        """
        Find all JSON scripts elements. If `application_json_ony` is set to
        `True`, only `<script type="application/json" />` will be returned.

        Else, a RegEx is applied to try to fetch all JSON data.

        :return: The list of found JSON objects.
        :rtype:  `typing.Generator[typing.Any, typing.Any, typing.Any]`
        """

        if application_json_only:
            return list(
                map(
                    lambda s: json.loads(s.text),
                    filter(
                        lambda s: (
                            s.has_attr("type") and s.attrs["type"] == "application/json"
                        ),
                        self.find_static_scripts_elements(),
                    ),
                )
            )

        for matchs in map(
            lambda s: _JSON_REGEX.findall(s.text),
            self.find_static_scripts_elements(),
        ):
            for m in matchs:
                if self._is_valid_json(m):
                    yield json.loads(m)

    def match_regex(
        self, regex: str | re.Pattern, match_each_line: bool = True
    ) -> list:
        """
        Check for matchs of RegEx into the text response.

        :param regex: The RegEx to match.
        :param match_each_line: Checks for matchs using `re.MULTILINE` flag.
        :type regex: `str` | `re.Pattern`
        :type match_each_line: `bool`
        :return: The list of all found matches
        :rtype: `list[typing.Any]`
        """

        if isinstance(regex, str):
            regex = re.compile(
                pattern=regex, flags=re.MULTILINE if match_each_line else 0
            )

        if not isinstance(regex, re.Pattern):
            raise ValueError("Invalid type for 'regex'.")

        return regex.findall(string=self._response.text)

    def to_json(self):
        """
        Tries to return the response in a JSON format.
        """

        return self._response.json()

    def handle_error(self, on_error_callback: OnErrorCallback):
        """
        Calls the `on_error_callback` function when an error is raised by the
        response.

        `on_error_callback` params :
        :param session: The session used to perform the request.
        :param response: The response received from the server.
        :param error: The raised error to handle.
        :type session: `requests.Session`
        :type response: `requests.Response`
        :type error: `urllib.error.HTTPError` | `requests.exceptions.HTTPError`
        :return: No output is expected, it can return anything.
        :rtype: `typing.Any`

        :param on_error_callback: The function to call which handles the error.
        :type on_error_callback: typing.Callable[[requests.Session, requests.Response, urllib.error.HTTPError | requests.exceptions.HTTPError], typing.Any]
        """

        if not isinstance(on_error_callback, typing.Callable):
            raise ValueError("Invalid type for 'on_error_callback'.")

        try:
            self._response.raise_for_status()
        except (urllib.error.HTTPError, requests.exceptions.HTTPError) as traceback:
            on_error_callback(self._session, self._response, traceback)
        return self
