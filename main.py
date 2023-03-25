from pathlib import Path
import os
import sys
import time
import requests


REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}
OUTPUT_FOLDER = "./threads"

THREAD_FROM = int(sys.argv[1])
THREAD_TO = int(sys.argv[2])


s = requests.Session()

for thread_number in range(THREAD_FROM, THREAD_TO + 1):
    thread_output_folder = os.path.join(OUTPUT_FOLDER, f"thread_{thread_number}")
    print(f"Trying to download all pages of thread {thread_number}")
    Path(thread_output_folder).mkdir(parents=True, exist_ok=True)

    page_number = 1

    while True:

        print(f"Downloading thread {thread_number} page {page_number}")

        try:
            res = s.get(
                f"https://www.dpreview.com/forums/thread/{thread_number}?page={page_number}",
                headers=REQUEST_HEADERS,
            )
        except requests.exceptions.RequestException as e:
            with open(os.path.join(OUTPUT_FOLDER, f"failed.txt"), "a+") as f:
                f.write(f"{thread_number}\t{e}\n")
            break

        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if res.status_code == 429:
                print(
                    "Made too much requests to the site in a short time, taking a 30-second rest"
                )
                print(e)
                time.sleep(30)
                continue
            with open(os.path.join(OUTPUT_FOLDER, f"failed.txt"), "a+") as f:
                f.write(f"{thread_number}\t{e}\n")

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
