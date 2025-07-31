import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph_supervisor import create_supervisor

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')



load_dotenv()

from langchain_core.messages import convert_to_messages


def pretty_print_message(message, indent=False):
    pretty_message = message.pretty_repr(html=True)
    if not indent:
        print(pretty_message)
        return

    indented = "\n".join("\t" + c for c in pretty_message.split("\n"))
    print(indented)


def pretty_print_messages(update, last_message=False):
    is_subgraph = False
    if isinstance(update, tuple):
        ns, update = update
        # skip parent graph updates in the printouts
        if len(ns) == 0:
            return

        graph_id = ns[-1].split(":")[0]
        print(f"Update from subgraph {graph_id}:")
        print("\n")
        is_subgraph = True

    for node_name, node_update in update.items():
        update_label = f"Update from node {node_name}:"
        if is_subgraph:
            update_label = "\t" + update_label

        print(update_label)
        print("\n")

        messages = convert_to_messages(node_update["messages"])
        if last_message:
            messages = messages[-1:]

        for m in messages:
            pretty_print_message(m, indent=is_subgraph)
        print("\n")


BRIGHT_DATA_API_KEY = os.getenv("BRIGHT_DATA_API_KEY")
OPENAI_API_KEY = os.getenv("ONEAPI_KEY")
async def run_agent(queruy: str):
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
    model = init_chat_model(model ="openai:gpt-4.1", api_key=OPENAI_API_KEY)
    stock_finder_agent = create_react_agent(model, tools, prompt="""
      You are a stock researcher analyst specializing in the Indian Stock market (NSE), Your Task is to select 2 promising , actively traded NSE-Listed stocks for short term trading (buy/sell) based on recent performance, news buz, volume or technical strength.
    Avoid penny stocks and illiquid stocks.
    Output should include  stock names, tickers, and brief reasoning for each choice.
    """, name="stock_finder_agent")
    
    market_data_agent = create_react_agent(model, tools, prompt="""
    You are a market data analyst for Indian stock listed on NSE. Given a list of stock tickers(eg RELIANCE, INFY), your task is to gather recent market information for each stock, including:
    - Current price
    - Previous close price
    - Today's Volume,
    - 7-day and 30-day price changes,
    - Basic technical indicators (e.g., RSI, MACD)
    - Any notable spikes in volume or price
                                           
    Return your findings in a structure and readable format for each  stock , suitable for further annalysis by a recommendaation engine. Use INR as currency. be concise but complete.
                                           
    """, name="market_data_agent")

    news_analyst_agent = create_react_agent(model, tools, prompt="""
    You are a financial news analyst. Given the names of tickers of Indian NSE stocks, your job is -
    1. Search for the latest news articles related to these stocks(past 3-5 days).
    2. Summarize the key points from these articles, focusing on any significant events, trends, or insights that could impact stock performance.
    3. Provide a brief sentiment analysis of the news (positive, negative, neutral) for each stock.
    4. Highlight how the news might affect short-term trading decisions for these stocks.
                                            
    Present your response in a clear, structured format - one section per stock.
    
    use bullete points where necessary. keep it concise, informative and analyst oriented
    """, name="news_analyst_agent")

    price_recommender_agent = create_react_agent(model, tools, prompt="""
    You are Trading  strategy advisor for the indian stock market. You are given:-
        - Recent market data (current price, previous close, volume, price changes, technical indicators) for a list of stocks.
        - Recent news summaries and sentiment analysis for these stocks.
                                                 
    Based on the information, for each stock -
        1. Recommend an action : Buy / SELL or hold
        2. Suggest a specific target price for entry or exit (INR)
        3. Briefly explain the reasoning behind your recommendation.
                                                 
    Your goal is to provide practical. near-term trading advice for the next trading day.
                                                
    Keep the response concise and clearly structured, with one section per stock. 
        
    """, name="price_recommender_agent")


    supervisor = create_supervisor(
        model=init_chat_model("openai:gpt-4.1", api_key=OPENAI_API_KEY),
        agents=[stock_finder_agent, market_data_agent, news_analyst_agent, price_recommender_agent],
        prompt=(
            "You are a supervisor managing four agents:\n"
            "- a stock_finder_agent. Assign research-related tasks to this agent and pick 2 promising NSE stocks\n"
            "- a market_data_agent. Assign tasks to fetch current market data (price, volume, trends)\n"
            "- a news_alanyst_agent. Assign task to search and summarize recent news\n"
            "- a price_recommender_agent. Assign task to give buy/sell decision with target price."
            "Assign work to one agent at a time, do not call agents in parallel.\n"
            "Do not do any work yourself.\n"
            "Be specific with 2 stock names and tickers.\n"
            "Make sure you complete till end of both stocks and do not ask for proceed in between the task."
        ),
        add_handoff_back_messages=True,
        output_mode="full_history",
    ).compile()

    for chunk in supervisor.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": queruy,
                }
            ]
            
        },
    ):
        pretty_print_messages(chunk, last_message=True)

    final_message_history = chunk["supervisor"]["messages"]
        


if __name__ == "__main__":
    asyncio.run(run_agent("Give me a good stock recommendation from NSE for short term trading"))