import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv()

root_agent = Agent(
    model="gemini-2.5-flash",
    name="weather_agent",
    description="A weather assistant powered by live MCP data.",
    instruction=(
        "You are a helpful weather assistant. "
        "Use the available weather tools to answer questions about "
        "current weather, forecasts, and conditions for any location. "
        "If one tool fails or has limitations, silently try another tool "
        "and only respond to the user with the final result. "
        "Do not explain tool limitations to the user. "
        "Respond in a clear, friendly format."
    ),
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx.cmd",        # .cmd fixes Windows npx issue
                    args=["-y", "@dangahagan/weather-mcp@latest"],
                    env={
                        "ENABLED_TOOLS": "full",
                        "CACHE_MAX_SIZE": "2000",
                        "LOG_LEVEL": "1",
                        **os.environ,
                    }
                ),
                timeout=60,
            )
        )
    ],
)