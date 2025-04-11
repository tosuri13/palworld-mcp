import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

response = requests.get("https://gamewith.jp/palworld/433556.html")
soup = BeautifulSoup(response.text, "html.parser")

for div in soup.select("ol div._head"):
    a = div.find("a")
    response = requests.get(a["href"])  # type: ignore

    file_name = a.text + ".html"  # type: ignore
    with open(Path("assets", "pals", file_name), "w", encoding="utf-8") as file:
        file.write(response.text)

    time.sleep(1)
    print(f"Saving file succeed: {file_name}")
