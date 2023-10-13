# LMDOIT (Let Me DOwnload IT)

**L**et **M**e **DO**wnload **IT** is a project which lets you schemafy your download process.

You'll be able to use plenty of methods for :
-   authentication (cookie, username:password, bearer token, ...),
-   parsing response (HTML Parser, regex, JSON server response, ...),
-   pass custom headers to certain routes,
-   add debugging steps by downloading response into files that you can freely open,
-   add custom starting points (instead of re-doing all requests, use a downloaded file as starting point)

# Example :

Here is an example about how to use the library :

```python
import sys
import urllib.error

import requests

from lmdoit import LMDOIT

def error_handler(session: requests.Session, response: requests.Response, error: urllib.error.HTTPError | requests.exceptions.HTTPError):
    print("Request headers :", session.headers)
    print("Request cookies :", session.cookies.get_dict())
    print("Response status code :", response.status_code)
    print("Response headers :", response.headers)
    print("Traceback :", error.args)
    sys.exit(1)

def main():
    response = (
        LMDOIT()
        .no_auth(url="https://datausa.io/api/data", method="GET")
        .set_url_params(params="drilldowns=Nation&measures=Population")
        .get_response()
        .handle_error(on_error_callback=error_handler)
        .save_response_for_debug("debug_data_here.json")
        .to_json()
    )

    print(response)


if __name__ == "__main__":
    main()
```