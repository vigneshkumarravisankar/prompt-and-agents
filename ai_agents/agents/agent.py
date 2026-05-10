import json
import os 
import requests

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from dotenv import load_dotenv
from google.adk.tools.function_tool import FunctionTool
# from .agents import *


load_dotenv()

if not (os.getenv("GOOGLE_API_KEY")):
    raise ValueError("GOOGLE_API_KEY is not set")


def fetch_json_placeholder_data(endpoint: str) -> str:
    """
    Fetches data from the JSONPlaceholder API.
    
    Args:
        endpoint: The resource endpoint to fetch data from. 
                  Valid endpoints include: posts, comments, albums, photos, todos, users.
                  Example: 'posts' will fetch from https://jsonplaceholder.typicode.com/posts
                  
    Returns:
        The JSON response from the API as a string.
    """
    base_url = "https://jsonplaceholder.typicode.com/"
    # Normalize endpoint
    endpoint = endpoint.strip("/")
    url = f"{base_url}{endpoint}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error fetching data: {str(e)}"

# Wrap the function in a FunctionTool
jsonplaceholder_tool = FunctionTool(fetch_json_placeholder_data)



albums_agent = LlmAgent(
    name="albums_agent",
    model="gemini-2.5-flash",
    instruction="You are a specialized agent for handling albums from JSONPlaceholder. Use the jsonplaceholder_tool with endpoint='albums' to retrieve and manage the 100 albums.",
    tools=[jsonplaceholder_tool]
)


comments_agent = LlmAgent(
    name="comments_agent",
    model="gemini-2.5-flash",
    instruction="You are a specialized agent for handling comments from JSONPlaceholder. Use the jsonplaceholder_tool with endpoint='comments' to retrieve and manage the 500 comments.",
    tools=[jsonplaceholder_tool]
)


photos_agent = LlmAgent(
    name="photos_agent",
    model="gemini-2.5-flash",
    instruction="You are a specialized agent for handling photos from JSONPlaceholder. Use the jsonplaceholder_tool with endpoint='photos' to retrieve and manage the 5000 photos.",
    tools=[jsonplaceholder_tool]
)

posts_agent = LlmAgent(
    name="posts_agent",
    model="gemini-2.5-flash",
    instruction="You are a specialized agent for handling posts from JSONPlaceholder. Use the jsonplaceholder_tool with endpoint='posts' to retrieve and manage the 100 posts.",
    tools=[jsonplaceholder_tool]
)

todos_agent = LlmAgent(
    name="todos_agent",
    model="gemini-2.5-flash",
    instruction="You are a specialized agent for handling todos from JSONPlaceholder. Use the jsonplaceholder_tool with endpoint='todos' to retrieve and manage the 200 todos.",
    tools=[jsonplaceholder_tool]
)

users_agent = LlmAgent(
    name="users_agent",
    model="gemini-2.5-flash",
    instruction="You are a specialized agent for handling users from JSONPlaceholder. Use the jsonplaceholder_tool with endpoint='users' to retrieve and manage the 10 users.",
    tools=[jsonplaceholder_tool]
)




root_agent = LlmAgent(
    name = "Json_Placeholder_Agent",
    model="gemini-2.5-flash",
    instruction="You are a master agent that coordinates fetching data from JSONPlaceholder. Delegate tasks to specialized agents for posts, comments, albums, photos, todos, and users.",
    sub_agents=[
        posts_agent,
        comments_agent,
        albums_agent,
        photos_agent,
        todos_agent,
        users_agent
    ]
)
