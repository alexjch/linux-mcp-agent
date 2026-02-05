
import sys
import asyncio
from linux_mcp_agent import agent


if __name__ == "__main__":
    exit_code = asyncio.run(agent.main())
    sys.exit(exit_code)
