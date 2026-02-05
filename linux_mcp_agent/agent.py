
import asyncio
from typing import Any
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec  # type: ignore[import-untyped]
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.ollama import Ollama   # type: ignore[import-untyped]


async def main() -> int:

    mcp_client = BasicMCPClient("/workspace/.bin/linux-mcp-server")
    mcp_tool_spec = McpToolSpec(client=mcp_client)
    tools = await mcp_tool_spec.to_tool_list_async()
    llm = Ollama(model="llama3.2:latest",
                 base_url="http://localhost:11434",
                 request_timeout=360.0
    )

    agent = FunctionAgent(
        tools=tools,
        llm=llm,
        system_prompt="You are a helpful assistant.",
    )

    response: Any = await agent.run("What processes are running right now in my system") # type: ignore
    print(response) # type: ignore

    return 0

if __name__ == "__main__":
    asyncio.run(main())
