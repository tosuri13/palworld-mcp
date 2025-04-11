from pathlib import Path

import duckdb

db_path = Path("assets/palworld.duckdb")
con = duckdb.connect(db_path)

con.execute("""
CREATE TABLE pals (
    name VARCHAR PRIMARY KEY,
    number VARCHAR,
    elements VARCHAR[],
    food INTEGER,
    hp INTEGER,
    attack INTEGER,
    defense INTEGER,
);
""")

comments = [
    (
        "name",
        "パルの名前",
    ),
    (
        "number",
        "パルの図鑑番号",
    ),
    (
        "elements",
        "パルの属性。無属性、炎属性、水属性、雷属性、地属性、草属性、氷属性、竜属性、闇属性のいずれかの値を取る",
    ),
    (
        "food",
        "パルの食事量。1から10までの値を取り、大きいほど食事量が多いことを表す",
    ),
    (
        "hp",
        "パルのヒットポイント",
    ),
    (
        "attack",
        "パルの攻撃力(ATK)",
    ),
    (
        "defense",
        "パルの防御力(DEF)",
    ),
]

for column_name, comment in comments:
    con.execute(f"COMMENT ON COLUMN pals.{column_name} IS '{comment}';")
