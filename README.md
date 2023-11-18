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
import json
import pathlib
import sys
import typing

sys.path.append("../")
import lmdoit

api = lmdoit.LMDOIT()


def find_all_vidoe_mp4_export(
    youtube_video_url: str,
) -> typing.Generator[dict, typing.Any, typing.Any]:
    youtube_response = api.no_auth(url=youtube_video_url, method="GET").get_response()
    all_youtube_json_objects = youtube_response.find_json_objects_from_script_elements()

    for data in all_youtube_json_objects:
        if not isinstance(data, dict) or not "streamingData" in data.keys():
            continue
        for fmt in data["streamingData"]["adaptiveFormats"]:
            if fmt.keys() >= {"width", "height", "url"}:
                yield dict(width=fmt["width"], height=fmt["height"], url=fmt["url"])


def main():
    youtube_video_url = "https://www.youtube.com/watch?v=[THE_VIDEO_CODE]"

    pathlib.Path("youtube_formats.json").write_text(
        json.dumps(list(find_all_vidoe_mp4_export(youtube_video_url=youtube_video_url)), indent=4)
    )

if __name__ == "__main__":
    main()
```

Which may result in this `youtube_formats.json` content :

```json
[
    {
        "width": 1920,
        "height": 1080,
        "url": "...",
    },
    {
        "width": 1920,
        "height": 1080,
        "url": "...",
    },
    {
        "width": 1280,
        "height": 720,
        "url": "...",
    },
    {
        "width": 1280,
        "height": 720,
        "url": "...",
    },
    {
        "width": 854,
        "height": 480,
        "url": "...",
    },
    {
        "width": 854,
        "height": 480,
        "url": "...",
    },
    {
        "width": 640,
        "height": 360,
        "url": "...",
    },
    {
        "width": 640,
        "height": 360,
        "url": "...",
    },
    {
        "width": 426,
        "height": 240,
        "url": "...",
    },
    {
        "width": 426,
        "height": 240,
        "url": "...",
    },
    {
        "width": 256,
        "height": 144,
        "url": "...",
    },
    {
        "width": 256,
        "height": 144,
        "url": "...",
    }
]
```