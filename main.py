from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import json
import httpx
import os
from bs4 import BeautifulSoup

load_dotenv()

mcp = FastMCP("docs")
USER_AGENT = "docs-app/1.0"
SERPER_URL = "https://google.serper.dev/search"

#return latest information using the following urls 
docs_url = {
    "langchain": "python.langchain.com/docs",
    "llama-index": "docs.llamaindex.ai/en/stable",
    "openai": "platform.openai.com/docs",
}

#we use SERPER for serach web for google serach API
'''
HELPER FUNCTIONS - search_web() and fetch_url()
async - allows to perform tasks without blocking other code execution (concurrency)
json dumps - to convert python objects (dict or list) into JSON format string
'''
async def search_web(query: str) -> dict | None:
    """Search the web for a query"""
    payload = json.dumps({'q': query, 'num': 2}) #query is sent as payload and focus on top 2 results

    #access SERPER API Key
    headers = {
        "X-API-KEY": os.getenv("SERPERAPI_KEY"),
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            #calling serper API and passing the query/payload to serach in web
            response = await client.post(
                SERPER_URL, headers=headers, data=payload, timeout=30.0      
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            return {"organic": []}


async def fetch_url(url: str):
    """fetch url for a query"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url, timeout=30.0
            )
            #parsing the repsonse
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
            return text
        except httpx.TimeoutException:
            return "Timeout Error"


#tool to get documents from the url
# when the agent trigers the serach web it get two responses using serach_web() and then fetch_url() opens it.

@mcp.tool() # decorator to convert function to actual tool so that it is compatible with MCP protocol (helps agent navigate with tools)
async def get_docs(query: str, library: str):
    #a description docstring is needed to any user/LLM to understand the tool
    """
    Search the docs for a given query and library (Supports Langchain, openai and llama-index)

    Params:
        query: the query to serach for
        library: library to serach in 
    
    Returns: 
        List of dictionaries containing source URLs and extracted text
    """
    if library not in docs_url:
        return ValueError(f"Library {library} not support by this tool.")
    
    query = f"site:{docs_url[library]} {query}" #format for seraching using SERPER
    result = await search_web(query)

    if len(result["organic"]) == 0:
        return "No result found"
    
    #for every result i have got we can fetch in oragnic part of the response (organic is a section in the JSON returned by SERPER)
    text=""
    for r in result['organic']:
        text += await fetch_url(r['link'])
    
    return text

# def main():
#     print("Hello from mcp-server!")

if __name__ == "__main__":
    mcp.run(transport='stdio')
