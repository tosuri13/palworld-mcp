from pathlib import Path
from typing import Annotated, TypedDict, cast

import duckdb
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek
from tabulate import tabulate


class Output(TypedDict):
    query: Annotated[str, "Federated SQL Query for Athena"]


def run(request: str):
    print(f"Request:\n{request}\n")

    db_path = Path("assets", "palworld.duckdb")
    con = duckdb.connect(db_path)

    table_name = "pals"
    query = f"""
        SELECT 
            column_name AS Column, 
            data_type AS Type, 
            COLUMN_COMMENT AS Comment
        FROM 
            information_schema.columns
        WHERE 
            table_name = '{table_name}'
        ORDER BY 
            ordinal_position;
    """
    results = con.execute(query).fetch_df()
    table_schema = tabulate(results, headers="keys", tablefmt="simple", showindex=False)  # type: ignore

    model = ChatDeepSeek(
        model="deepseek-chat",
        temperature=0.0,
    )
    model = model.with_structured_output(Output)

    messages = [
        SystemMessage(
            "あなたは、「Palworld」と呼ばれるPCゲームのデータ分析を行うデータアナリストです。\n"
            "これから与えられるスキーマを参照して、ユーザのリクエストに対する適切なSQLクエリを生成してください。\n"
        ),
        HumanMessage(
            f"以下に利用可能なテーブルのスキーマを与えます。\n"
            f"\n"
            f"# テーブル その1\n"
            f"- テーブル名: {table_name}\n"
            f"- テーブルのスキーマ\n"
            f"{table_schema}\n"
            f"\n"
            f"以下にユーザからのリクエストを与えます。\n"
            f"- {request}"
        ),
    ]

    response = model.invoke(messages)
    query = cast(Output, response)["query"]
    print(f"Query:\n{query}\n")

    results = con.execute(query).fetch_df()
    print("Results:")
    print(tabulate(results, headers="keys", tablefmt="simple", showindex=False))  # type: ignore


if __name__ == "__main__":
    run("パルの各属性ごとに食事量の平均を求めたい")
