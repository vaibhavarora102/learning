import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model

load_dotenv()


BRIGHT_DATA_API_KEY = os.getenv("BRIGHT_DATA_API_KEY")
ONEAPI_KEY = os.getenv("ONEAPI_KEY")
async def run_agent():
    # Ensure the environment variables are set
    client = MultiServerMCPClient(
        {
            "brightdata": {
                "command": "npx",
                "args": ["@brightdata/mcp"],
                "env": {
                    "API_TOKEN": BRIGHT_DATA_API_KEY,
                    "WEB_UNLOCKER_ZONE": "unblocker",
                    "BROWSER_ZONE": "scraping_browser",
                },
                "transport": "stdio",
            },
        }
    )
    tools = await client.get_tools()
    model = init_chat_model(model ="openai:gpt-4.1", api_key=ONEAPI_KEY)
    agent = create_react_agent(model, tools, prompt="You are a web search agent with aaccess to brightdata tools to get latest data")
    agent_response = await agent.ainvoke(
        {"messages": "What is Trumps latest announcement?"}
        
    )
    print("Agent response:", agent_response["messages"][-1].content)



if __name__ == "__main__":
    asyncio.run(run_agent())