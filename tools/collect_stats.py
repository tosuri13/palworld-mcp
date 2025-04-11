import os
from pathlib import Path

from bs4 import BeautifulSoup


def extract_stats(path: Path):
    soup = BeautifulSoup(path.read_text(), "html.parser")

    name = path.stem
    number = soup.find("th", string="図鑑No").find_next("td").text[3:]  # type: ignore
    elements = [
        a.text
        for a in soup.find("th", string="タイプ").find_next("td").find_all("a")  # type: ignore
    ]
    food = int(soup.find("th", string="食事量").find_next("td").find("div")["data-num"])  # type: ignore
    hp = int(soup.find("th", string="HP").find_next("td").text)  # type: ignore
    attack = int(soup.find("th", string="攻撃").find_next("td").text)  # type: ignore
    defense = int(soup.find("th", string="防御").find_next("td").text)  # type: ignore

    return {
        "name": name,
        "number": number,
        "elements": elements,
        "food": food,
        "hp": hp,
        "attack": attack,
        "defense": defense,
    }


for root, dirs, files in os.walk(Path("assets", "pals")):
    for file in files:
        stats = extract_stats(Path(root, file))
        print(stats)
