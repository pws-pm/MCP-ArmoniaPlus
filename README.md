# MCP Server for ArmoníaPlus

A Model Context Protocol (MCP) server that enables Claude AI to control ArmoníaPlus devices through its local API.

## Overview

This server acts as a bridge between Claude AI and the ArmoníaPlus audio control software. It allows Claude to query and control devices managed by ArmoníaPlus through the Model Context Protocol (MCP).

## Prerequisites

1. **ArmoníaPlus Software** installed on your system
2. **ARA API enabled** in ArmoníaPlus:
   - Open ArmoníaPlus
   - Go to Options/Settings
   - Enable the ARA API option
   - Note the API port (default: 40402)

3. **Python 3.8+** installed on your system
4. **uv** package manager installed:
   ```bash
   pip install uv
   ```

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/mcp-armonia.git
   cd mcp-armonia
   ```

2. Create and configure the `.env` file:
   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file with your ArmoníaPlus API information:
   ```
   ARMONIA_API_URL=http://your-armonia-ip:40402/api/ARA
   ARMONIA_AUTH_TOKEN=your-auth-token
   ```

4. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

## Running the Server

You can run the server directly:

```bash
uv run run_mcp_server.py
```

## Connecting with Claude Desktop

1. Install Claude Desktop from https://claude.ai/desktop

2. Create or edit the Claude Desktop configuration file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

3. Add the following configuration:

```json
{
    "mcpServers": {
        "armonia": {
            "command": "/full/path/to/uv",
            "args": [
                "--directory",
                "/full/path/to/mcp-armonia",
                "run",
                "run_mcp_server.py"
            ]
        }
    }
}
```

Example (replace with your actual paths):
```json
{
    "mcpServers": {
        "armonia": {
            "command": "/Users/yourusername/.local/bin/uv",
            "args": [
                "--directory",
                "/Users/yourusername/path/to/mcp-armonia",
                "run",
                "run_mcp_server.py"
            ]
        }
    }
}
```

4. Restart Claude Desktop

## Available Tools in Claude

Once connected, Claude will have access to the following tools:

- **get_system_status**: View all devices in your ArmoníaPlus system
- **get_online_devices**: See only online devices
- **get_device_details**: Get detailed information about a specific device
- **set_device_gain**: Adjust the gain for a device channel

## Troubleshooting

- **ENOENT Error**: Make sure the path to `uv` is correct. Find it with `which uv`
- **Connection Failed**: Verify ArmoníaPlus is running and the API is enabled
- **No Devices Shown**: Check your network connectivity to the ArmoníaPlus system

## License

MIT License

## Acknowledgements

This project is part of the Powersoft Audio ecosystem and adheres to the [Model Context Protocol](https://modelcontextprotocol.io/) specification. 