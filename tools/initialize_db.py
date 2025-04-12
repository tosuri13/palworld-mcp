import os
from pathlib import Path
from typing import Callable

import duckdb
from bs4 import BeautifulSoup
from pydantic import BaseModel

db_path = Path("assets", "palworld.duckdb")
os.remove(db_path)
con = duckdb.connect(db_path)


class ColumnDefenition(BaseModel):
    name: str
    type: str
    comment: str
    is_pk: bool = False


def extract_pal(path: Path) -> dict:
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


def create_db(table_name: str, columns: list[ColumnDefenition]):
    sql = f"CREATE TABLE {table_name} ("
    sql += ", ".join(
        [
            f"{column.name} {column.type}{' PRIMARY KEY' if column.is_pk else ''}"
            for column in columns
        ]
    )
    sql += ");"
    con.execute(sql)

    for column in columns:
        con.execute(
            f"COMMENT ON COLUMN {table_name}.{column.name} IS '{column.comment}';"
        )


def insert(table_name: str, extractor: Callable[[Path], dict]):
    for root, _, files in os.walk(Path("assets", "pals")):
        for file in files:
            record = extractor(Path(root, file))
            sql = f"INSERT INTO {table_name} VALUES ({', '.join([f'${i + 1}' for i, _ in enumerate(record)])})"
            con.execute(sql, record.values())


create_db(
    table_name="pals",
    columns=[
        ColumnDefenition(
            name="name",
            type="VARCHAR",
            comment="パルの名前",
            is_pk=True,
        ),
        ColumnDefenition(
            name="number",
            type="VARCHAR",
            comment="パルの図鑑番号",
        ),
        ColumnDefenition(
            name="elements",
            type="VARCHAR[]",
            comment="パルの属性。無属性、炎属性、水属性、雷属性、地属性、草属性、氷属性、竜属性、闇属性のいずれかの値を取る",
        ),
        ColumnDefenition(
            name="food",
            type="INTEGER",
            comment="パルの食事量。1から10までの値を取り、大きいほど食事量が多いことを表す",
        ),
        ColumnDefenition(
            name="hp",
            type="INTEGER",
            comment="パルのヒットポイント",
        ),
        ColumnDefenition(
            name="attack",
            type="INTEGER",
            comment="パルの攻撃力(ATK)",
        ),
        ColumnDefenition(
            name="defense",
            type="INTEGER",
            comment="パルの防御力(DEF)",
        ),
    ],
)
insert(table_name="pals", extractor=extract_pal)
