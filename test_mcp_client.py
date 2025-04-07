#!/usr/bin/env python3
"""
Test client for the MCP Server for ArmoníaPlus
This script simulates an LLM client calling the MCP server tools
"""

import os
import json
import subprocess
import time
import sys
from typing import Dict, Any, Optional, List

class MCPTestClient:
    """Simple test client for MCP that communicates over stdio with the server"""
    
    def __init__(self, command: List[str]):
        """
        Initialize the MCP test client
        
        Args:
            command: The command to start the MCP server
        """
        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        self.request_id = 0
        self.initialize()
        
    def initialize(self):
        """Initialize the MCP connection"""
        init_msg = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "0.1.0"
                }
            }
        }
        self._send_message(init_msg)
        response = self._read_response()
        print(f"Server initialized: {response}")
        
        # Request tools
        self.request_id += 1
        tools_msg = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/list",
            "params": {}
        }
        self._send_message(tools_msg)
        self.tools_response = self._read_response()
        
        print("\n=== Available Tools ===")
        for tool in self.tools_response.get("result", {}).get("tools", []):
            print(f"- {tool['name']}: {tool['description']}")
        print("======================\n")
    
    def _send_message(self, message: Dict[str, Any]):
        """Send a message to the MCP server"""
        json_str = json.dumps(message)
        content_length = len(json_str)
        
        self.process.stdin.write(f"Content-Length: {content_length}\r\n")
        self.process.stdin.write("\r\n")
        self.process.stdin.write(json_str)
        self.process.stdin.flush()
    
    def _read_response(self) -> Dict[str, Any]:
        """Read a response from the MCP server"""
        content_length = None
        
        # Read headers
        while True:
            line = self.process.stdout.readline().strip()
            if not line:
                break
                
            if line.startswith("Content-Length:"):
                content_length = int(line.split(":", 1)[1].strip())
        
        if content_length is None:
            raise ValueError("No Content-Length header in response")
            
        # Read the JSON content
        content = self.process.stdout.read(content_length)
        return json.loads(content)
    
    def call_tool(self, tool_name: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Call an MCP tool
        
        Args:
            tool_name: The name of the tool to call
            params: The parameters to pass to the tool
            
        Returns:
            The tool's response
        """
        self.request_id += 1
        
        tool_msg = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/use",
            "params": {
                "name": tool_name,
                "parameters": params or {}
            }
        }
        
        self._send_message(tool_msg)
        return self._read_response()
    
    def shutdown(self):
        """Close the server connection gracefully"""
        self.request_id += 1
        shutdown_msg = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "shutdown",
            "params": {}
        }
        self._send_message(shutdown_msg)
        self._read_response()
        
        # Send exit notification
        exit_msg = {
            "jsonrpc": "2.0",
            "method": "exit",
            "params": {}
        }
        self._send_message(exit_msg)
        
        # Close the process
        self.process.terminate()
        
        # Collect stderr output
        stderr = self.process.stderr.read()
        if stderr.strip():
            print("\nServer stderr output:")
            print(stderr)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

def read_tool_inputs(tool_name: str) -> Dict[str, Any]:
    """Prompt for tool input parameters based on tool name"""
    if tool_name == "get_system_status" or tool_name == "get_online_devices":
        # These tools don't require parameters
        return {}
    
    elif tool_name == "get_device_details":
        device_id = input("Enter device ID: ")
        return {"device_id": device_id}
    
    elif tool_name == "set_device_gain":
        device_id = input("Enter device ID: ")
        channel = int(input("Enter channel number: "))
        value = float(input("Enter gain value: "))
        return {
            "device_id": device_id,
            "channel": channel,
            "value": value
        }
    
    else:
        print(f"Unknown tool: {tool_name}")
        return {}

def main():
    """Run the MCP client test"""
    
    script_path = os.path.dirname(os.path.abspath(__file__))
    
    # Command to start the MCP server
    command = [
        sys.executable,
        os.path.join(script_path, "mcp_server_armonia.py")
    ]
    
    with MCPTestClient(command) as client:
        while True:
            print("\nChoose a tool to test:")
            print("1. get_system_status")
            print("2. get_online_devices")
            print("3. get_device_details")
            print("4. set_device_gain")
            print("0. Exit")
            
            choice = input("\nEnter choice (0-4): ")
            
            if choice == "0":
                break
                
            tool_mapping = {
                "1": "get_system_status",
                "2": "get_online_devices", 
                "3": "get_device_details",
                "4": "set_device_gain"
            }
            
            if choice in tool_mapping:
                tool_name = tool_mapping[choice]
                params = read_tool_inputs(tool_name)
                
                print(f"\nCalling {tool_name}...")
                response = client.call_tool(tool_name, params)
                
                print("\nResponse:")
                if "result" in response:
                    print(response["result"])
                else:
                    print(f"Error: {response.get('error', 'Unknown error')}")
            else:
                print("Invalid choice, please try again.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 