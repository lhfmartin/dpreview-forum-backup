from pathlib import Path
import os
import sys
import requests


REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

THREAD_FROM = int(sys.argv[1])
THREAD_TO = int(sys.argv[2])


for thread_number in range(THREAD_FROM, THREAD_TO + 1):
    thread_output_folder = f"./threads/thread_{thread_number}"
    print(f"Trying to download all pages of thread {thread_number}")
    Path(thread_output_folder).mkdir(parents=True, exist_ok=True)

    page_number = 1

    while True:

        print(f"Downloading thread {thread_number} page {page_number}")

        res = requests.get(
            f"https://www.dpreview.com/forums/thread/{thread_number}?page={page_number}",
            headers=REQUEST_HEADERS,
        )
        res.raise_for_status()

        page_html = res.text
        with open(
            os.path.join(thread_output_folder, f"page_{page_number}.html"), "w+"
        ) as f:
            f.write(page_html)
        if 'class="next enabled"' in page_html:
            page_number += 1
        else:
            break

    print(
        f"Saved page 1 - {page_number} of thread {thread_number} to {os.path.abspath(thread_output_folder)}"
    )
