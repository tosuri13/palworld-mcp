import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool


async def serve() -> None:
    server = Server("palworld-mcp")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return []

    @server.call_tool()
    async def call_tool(name: str, args: dict) -> list[TextContent]:
        match name:
            case _:
                raise ValueError(f"Unknown tool: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            options,
            raise_exceptions=True,
        )


if __name__ == "__main__":
    asyncio.run(serve())
