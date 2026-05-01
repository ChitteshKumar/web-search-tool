# MCP Docs Server

A Model Context Protocol (MCP) server that provides tools for searching and retrieving documentation from popular AI/LLM libraries. This server uses SERPER API for web search and BeautifulSoup for content extraction.

## Features

- **Web Search Integration**: Uses SERPER API to search documentation across supported libraries
- **Multiple Library Support**: Search docs for LangChain, OpenAI, and LlamaIndex
- **Async Operations**: Built with async/await for efficient concurrent requests
- **MCP Protocol Compatible**: Works with any MCP-compatible client

## Supported Libraries

- **LangChain**: `langchain` - https://python.langchain.com/docs
- **OpenAI**: `openai` - https://platform.openai.com/docs
- **LlamaIndex**: `llama-index` - https://docs.llamaindex.ai/en/stable

## Prerequisites

- Python 3.12 or higher
- SERPER API key (get yours at https://serper.dev)

## Installation

1. Install dependencies:
```bash
uv pip install -e .
```

2. Configure environment variables:

Create a `.env` file in the `mcp-server` directory:
```env
SERPERAPI_KEY=your_api_key_here
```

## Usage

### Running the Server

Run the MCP server using:
```bash
uv run main.py
```

Or with stdio transport:
```bash
uv run main.py --transport=stdio
```

### Using as an MCP Tool

The server provides a `get_docs` tool with the following parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | The search query |
| `library` | string | Library name (langchain, openai, llama-index) |

Example usage in code:
```python
result = await get_docs("quickstart", "langchain")
```

## Debugging

To test and debug the MCP server, use the inspector:
```bash
npx @modelcontextprotocol/inspector uv run main.py
```

## Configuration

| Environment Variable | Required | Description |
|--------------------|----------|-------------|
| `SERPERAPI_KEY` | Yes | API key for SERPER web search |

## License

MIT License
