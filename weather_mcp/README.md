# Weather MCP Agent using Google ADK + Gemini + MCP

A hands-on project demonstrating how to integrate a Model Context Protocol (MCP) server with Google ADK using Gemini models.

This project uses:

- Google ADK
- Gemini 2.0/2.5 Flash
- Weather MCP Server
- Python
- Node.js + npx

---

# Project Overview

This agent can:

- Fetch real-time weather
- Compare weather between cities
- Check rain forecasts
- Use live MCP tools automatically

The MCP server exposes tools and Google ADK automatically discovers and uses them through `MCPToolset`.

---

# Architecture

```text
User Prompt
    ↓
Google ADK Agent
    ↓
MCPToolset
    ↓
Weather MCP Server
    ↓
Live Weather Data
    ↓
Gemini Response
```

---

# Prerequisites

Install the following before starting:

## 1. Python

Install Python 3.10+

Verify:

```bash
python --version
```

---

## 2. Node.js

Install Node.js LTS version.

Download:

https://nodejs.org

Verify:

```bash
npx --version
```

---

# Project Setup

---

# Step 1 — Create Project Folder

```bash
mkdir weather_agent
cd weather_agent
```

---

# Step 2 — Create Virtual Environment

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

After activation you should see:

```bash
(venv)
```

---

# Step 3 — Install Dependencies

```bash
pip install google-adk python-dotenv
```

---

# Step 4 — Create Project Structure

Create the following structure:

```text
weather_agent/
│
├── venv/
│
└── weather_agent/
    ├── __init__.py
    ├── agent.py
    └── .env
```

---

# IMPORTANT — Why Inner weather_agent Folder?

Google ADK expects:

```text
Parent Folder
    └── agents directory
            └── actual agent
```

So the inner `weather_agent/` is the actual ADK agent.

Without this structure ADK may accidentally detect `venv` as the agent.

---

# Step 5 — Create Gemini API Key

Open:

https://aistudio.google.com/apikey

Create API key.

---

# Step 6 — Configure .env

Inside:

```text
weather_agent/weather_agent/.env
```

Add:

```env
GOOGLE_API_KEY=your_api_key_here
```

---

# Step 7 — Create __init__.py

Inside:

```text
weather_agent/weather_agent/__init__.py
```

Add:

```python
from . import agent
```

---

# Step 8 — Create agent.py

Inside:

```text
weather_agent/weather_agent/agent.py
```

Paste:

```python
import os
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioConnectionParams,
)

from mcp import StdioServerParameters

load_dotenv()

root_agent = Agent(
    model="gemini-2.0-flash",
    name="weather_agent",
    description="Weather assistant powered by live MCP data.",
    instruction="""
    You are a helpful weather assistant.

    When the user asks about weather for any city or location,
    use the available weather tools to fetch real-time data
    and respond clearly.
    """,
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx.cmd",
                    args=[
                        "-y",
                        "@dangahagan/weather-mcp@latest"
                    ],
                    env={
                        "ENABLED_TOOLS": "full",
                        "CACHE_MAX_SIZE": "2000",
                        "LOG_LEVEL": "1",
                        **os.environ,
                    }
                )
            )
        )
    ],
)
```

---

# Why npx.cmd Instead of npx?

On Windows:

```python
command="npx"
```

may fail or hang.

Use:

```python
command="npx.cmd"
```

This fixes most Windows MCP issues.

---

# Step 9 — Run the Agent

Go to parent directory:

```bash
cd ..
```

Example:

```text
E:\
```

Run:

```bash
adk web weather_agent
```

---

# Successful Output

You should see:

```text
ADK Web Server started

http://127.0.0.1:8000
```

---

# Step 10 — Open Browser

Open:

```text
http://127.0.0.1:8000
```

---

# Test Prompts

Try:

```text
What's the weather in Chennai?
```

```text
Will it rain in Coimbatore today?
```

```text
Compare weather in Delhi and Mumbai
```

---

# Common Errors and Fixes

---

# Error 1 — npx not found

## Error

```text
npx not found
```

## Fix

Install Node.js:

https://nodejs.org

Restart VS Code.

Verify:

```bash
npx --version
```

---

# Error 2 — dotenv module missing

## Error

```text
ModuleNotFoundError: dotenv
```

## Fix

```bash
pip install python-dotenv
```

---

# Error 3 — google.adk missing

## Error

```text
ModuleNotFoundError: google.adk
```

## Fix

```bash
pip install google-adk
```

---

# Error 4 — ADK loads venv as agent

## Problem

ADK detects:

```text
venv
```

instead of:

```text
weather_agent
```

## Cause

Wrong folder structure.

## Correct Structure

```text
weather_agent/
│
├── venv/
│
└── weather_agent/
    ├── agent.py
```

---

# Error 5 — Agent not found

## Error

```text
Agent 'weather_agent' not found
```

## Fix

Run from parent directory:

```bash
cd ..
adk web weather_agent
```

NOT from inside the inner agent folder.

---

# Error 6 — MCP Timeout

## Error

```text
Failed to create MCP session
```

or tool hangs forever.

## Fix

Open:

```text
venv/Lib/site-packages/google/adk/tools/mcp_tool/mcp_session_manager.py
```

Find:

```python
read_timeout_seconds=timedelta(seconds=5)
```

Change to:

```python
read_timeout_seconds=timedelta(seconds=60)
```

Save and restart server.

---

# Error 7 — Browser Opens Wrong App

## Problem

Browser URL shows:

```text
?app=venv
```

## Fix

Change URL manually:

```text
http://127.0.0.1:8000/dev-ui/?app=weather_agent
```

---

# Using Gemini 2.5 Flash

You can also use:

```python
model="gemini-2.5-flash"
```

or:

```python
model="gemini-2.5-flash-preview-05-14"
```

But for workshops:

```python
gemini-2.0-flash
```

is simpler and more stable.

---

# How MCP Works Internally

```text
ADK Agent
    ↓
MCPToolset
    ↓
Starts MCP Server using npx
    ↓
Discovers tools automatically
    ↓
Gemini decides tool usage
    ↓
Tool returns weather data
    ↓
Agent responds naturally
```

---

# Workshop Demo Flow

Recommended demo sequence:

1. Explain MCP concept
2. Show project structure
3. Run ADK server
4. Open browser UI
5. Ask weather questions
6. Show live tool calling
7. Explain MCP tool discovery
8. Explain how Gemini chooses tools

---

# Recommended Student Exercises

Students can extend this project by:

- Adding stock MCP servers
- Adding GitHub MCP tools
- Adding calculator tools
- Adding memory support
- Building multi-agent systems
- Using Gemini 2.5 Pro

---

# Final Notes

This project demonstrates:

- MCP Integration
- Tool Calling
- Google ADK
- Gemini APIs
- AI Agents
- Live External Tools

without manually writing tools.

Google ADK automatically converts MCP tools into usable AI agent tools.

---

# References

Google ADK:
https://google.github.io/adk-docs/

Google AI Studio:
https://aistudio.google.com/

Weather MCP:
https://www.npmjs.com/package/@dangahagan/weather-mcp

Model Context Protocol:
https://modelcontextprotocol.io/

