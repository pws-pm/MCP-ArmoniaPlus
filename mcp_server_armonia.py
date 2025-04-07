#!/usr/bin/env python3
"""
MCP Server for ArmoníaPlus using the official MCP SDK
"""

import json
import requests
import os
import logging
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-server-armonia")

# Initialize FastMCP server
mcp = FastMCP("armonia")

# Constants for ArmoníaPlus API
ARMONIA_API_URL = os.environ.get("ARMONIA_API_URL", "http://localhost:40402/api/ARA")
ARMONIA_AUTH_TOKEN = os.environ.get("ARMONIA_AUTH_TOKEN", "fcb0d2ee-9179-4968-8799-690fd242d530")

# API Helper function
def call_armonia_api(endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Helper function to call the ArmoníaPlus API"""
    headers = {"authClientToken": ARMONIA_AUTH_TOKEN}
    url = f"{ARMONIA_API_URL}/{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
            
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error calling ArmoníaPlus API: {str(e)}")
        raise Exception(f"Error communicating with ArmoníaPlus API: {str(e)}")

# MCP Tools

@mcp.tool()
async def get_system_status() -> str:
    """Get the status of all devices in the ArmoníaPlus system"""
    try:
        system_status = call_armonia_api("GetSystemStatus")
        devices = system_status.get("devices", [])
        
        if not devices:
            return "No devices found in the ArmoníaPlus system."
            
        status_report = []
        for device in devices:
            status = "Online" if device.get("isOnline", False) else "Offline"
            status_report.append(
                f"Device: {device.get('name', 'Unnamed')} ({device.get('model', 'Unknown')})\n"
                f"Status: {status}\n"
                f"ID: {device.get('uniqueID', 'Unknown')}\n"
                f"IP: {device.get('ipAddress', 'Not assigned')}\n"
                f"Firmware: {device.get('firmwareVersion', 'Unknown')}\n"
            )
        
        return "\n---\n".join(status_report)
    except Exception as e:
        return f"Error getting system status: {str(e)}"

@mcp.tool()
async def get_online_devices() -> str:
    """Get only the online devices in the ArmoníaPlus system"""
    try:
        system_status = call_armonia_api("GetSystemStatus")
        devices = system_status.get("devices", [])
        online_devices = [d for d in devices if d.get("isOnline", False)]
        
        if not online_devices:
            return "No online devices found."
            
        status_report = []
        for device in online_devices:
            status_report.append(
                f"Device: {device.get('name', 'Unnamed')} ({device.get('model', 'Unknown')})\n"
                f"ID: {device.get('uniqueID', 'Unknown')}\n"
                f"IP: {device.get('ipAddress', 'Not assigned')}\n"
                f"Firmware: {device.get('firmwareVersion', 'Unknown')}\n"
            )
        
        return "\n---\n".join(status_report)
    except Exception as e:
        return f"Error getting online devices: {str(e)}"

@mcp.tool()
async def get_device_details(device_id: str) -> str:
    """Get detailed information about a specific device
    
    Args:
        device_id: The unique ID of the device to get details for
    """
    try:
        system_status = call_armonia_api("GetSystemStatus")
        devices = system_status.get("devices", [])
        
        for device in devices:
            if device.get("uniqueID") == device_id:
                return (
                    f"Device Details:\n"
                    f"Name: {device.get('name', 'Unnamed')}\n"
                    f"Model: {device.get('model', 'Unknown')}\n"
                    f"ID: {device.get('uniqueID', 'Unknown')}\n"
                    f"IP: {device.get('ipAddress', 'Not assigned')}\n"
                    f"Status: {'Online' if device.get('isOnline', False) else 'Offline'}\n"
                    f"Linked: {'Yes' if device.get('isLinked', False) else 'No'}\n"
                    f"Firmware: {device.get('firmwareVersion', 'Unknown')}\n"
                    f"Serial: {device.get('serialNumber', 'Unknown')}"
                )
        
        return f"Device with ID {device_id} not found."
    except Exception as e:
        return f"Error getting device details: {str(e)}"

@mcp.tool()
async def set_device_gain(device_id: str, channel: int, value: float) -> str:
    """Set the gain for a specific device channel
    
    Args:
        device_id: The unique ID of the device
        channel: The channel number to adjust (0-based)
        value: The gain value to set
    """
    try:
        data = {
            "UniqueID": device_id,
            "Channel": str(channel),
            "Value": str(value)
        }
        response = call_armonia_api("SetAdvancedEqGain", method="POST", data=data)
        return f"Successfully set gain for device {device_id}, channel {channel} to {value}"
    except Exception as e:
        return f"Error setting device gain: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio') 