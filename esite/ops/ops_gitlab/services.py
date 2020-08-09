import requests
import tempfile

from django.core import files


class GitLabScraper:
    def __init__(self, token):
        self.headers = {"Private-Token": token}

    def get(self, url, **kwargs):
        resp = requests.get((url), headers=self.headers)

        page = resp.headers.get("X-Page")
        next_page = resp.headers.get("X-Next-Page")

        page = int(page) if page and page.isdigit() else 0
        next_page = int(next_page) if next_page and next_page.isdigit() else 0

        while page < next_page:
            self.get(url, page=page + 1)

    def gen_request(self, url, **kwargs):
        options = {"goto_page": 0, "optional_parameter": ""}
        options.update(kwargs)
        print("req:", url, kwargs, self.headers)
        resp = requests.get(
            (
                f"{url}?page={options['goto_page']}&per_page=100&{options['optional_parameter']}"
            ),
            headers=self.headers,
        )

        page = resp.headers.get("X-Page")
        next_page = resp.headers.get("X-Next-Page")

        page = int(page) if page and page.isdigit() else 0
        next_page = int(next_page) if next_page and next_page.isdigit() else 0

        yield resp.json()

        if page < next_page:
            yield from self.gen_request(url, goto_page=next_page)


def create_image_from_url(image_url: str) -> (str, files.File):
    request = requests.get(image_url, stream=True)

    # Was the request OK?
    if request.status_code != requests.codes["ok"]:
        # Nope, error handling, skip file etc etc etc
        raise "Not a valid URL"

    # Get the filename from the url, used for saving later
    file_name = image_url.split("/")[-1]

    # Create a temporary file
    lf = tempfile.NamedTemporaryFile()

    # Read the streamed image in sections
    for block in request.iter_content(1024 * 8):

        # If no more file then stop
        if not block:
            break

        # Write image block to temporary file
        lf.write(block)

    return (file_name, files.File(lf))
