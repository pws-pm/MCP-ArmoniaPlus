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
def call_armonia_api(endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None, timeout: int = 10) -> Dict[str, Any]:
    """Helper function to call the ArmoníaPlus API"""
    headers = {"authClientToken": ARMONIA_AUTH_TOKEN}
    url = f"{ARMONIA_API_URL}/{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=timeout)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
            
        response.raise_for_status()
        result = response.json()
        
        # Check for error codes in the response as done in check_armonia.py
        if result.get("ERROR_CODE"):
            error_code = result.get("ERROR_CODE")
            error_desc = result.get("ERROR_DESCRIPTION", "No description provided")
            logger.error(f"API Error: {error_code} - {error_desc}")
            raise Exception(f"ArmoníaPlus API Error: {error_code} - {error_desc}")
            
        return result
    except requests.RequestException as e:
        logger.error(f"Error calling ArmoníaPlus API: {str(e)}")
        raise Exception(f"Error communicating with ArmoníaPlus API: {str(e)}")

# MCP Tools

@mcp.tool()
async def get_system_status() -> str:
    """Get the status of all devices in the ArmoníaPlus system"""
    try:
        system_status = call_armonia_api("GetSystemStatus")
        
        # Try to locate devices with correct capitalization like in check_armonia.py
        devices = None
        if "Devices" in system_status:
            devices = system_status.get("Devices", [])
        # Fallbacks for API inconsistency
        elif "devices" in system_status:
            devices = system_status.get("devices", [])
        elif "DEVICES" in system_status:
            devices = system_status.get("DEVICES", [])
        else:
            return "No 'Devices' field found in the API response."
        
        if not devices:
            return "No devices found in the ArmoníaPlus system."
            
        status_report = []
        for device in devices:
            # Handle different field name cases like in check_armonia.py
            model = device.get("Model") or device.get("model") or device.get("MODEL") or "Unknown Model"
            device_id = device.get("UniqueID") or device.get("uniqueID") or device.get("UNIQUE_ID") or "Unknown ID"
            is_online = device.get("IsOnline", device.get("isOnline", device.get("IS_ONLINE", False)))
            name = device.get("Name") or device.get("name") or "Unnamed"
            ip_address = device.get("IpAddress") or device.get("ipAddress") or device.get("IP_ADDRESS") or "Not assigned"
            firmware = device.get("FirmwareVersion") or device.get("firmwareVersion") or device.get("FIRMWARE_VERSION") or "Unknown"
            
            status = "Online" if is_online else "Offline"
            status_report.append(
                f"Device: {name} ({model})\n"
                f"Status: {status}\n"
                f"ID: {device_id}\n"
                f"IP: {ip_address}\n"
                f"Firmware: {firmware}\n"
            )
        
        return "\n---\n".join(status_report)
    except Exception as e:
        return f"Error getting system status: {str(e)}"

@mcp.tool()
async def get_online_devices() -> str:
    """Get only the online devices in the ArmoníaPlus system"""
    try:
        system_status = call_armonia_api("GetSystemStatus")
        
        # Try to locate devices with correct capitalization
        devices = None
        if "Devices" in system_status:
            devices = system_status.get("Devices", [])
        # Fallbacks for API inconsistency
        elif "devices" in system_status:
            devices = system_status.get("devices", [])
        elif "DEVICES" in system_status:
            devices = system_status.get("DEVICES", [])
        else:
            return "No 'Devices' field found in the API response."
        
        # Use the same field handling as in check_armonia.py
        online_devices = [d for d in devices if d.get("IsOnline", d.get("isOnline", d.get("IS_ONLINE", False)))]
        
        if not online_devices:
            return "No online devices found."
            
        status_report = []
        for device in online_devices:
            # Handle different field name cases
            model = device.get("Model") or device.get("model") or device.get("MODEL") or "Unknown Model"
            device_id = device.get("UniqueID") or device.get("uniqueID") or device.get("UNIQUE_ID") or "Unknown ID"
            name = device.get("Name") or device.get("name") or "Unnamed"
            ip_address = device.get("IpAddress") or device.get("ipAddress") or device.get("IP_ADDRESS") or "Not assigned"
            firmware = device.get("FirmwareVersion") or device.get("firmwareVersion") or device.get("FIRMWARE_VERSION") or "Unknown"
            
            status_report.append(
                f"Device: {name} ({model})\n"
                f"ID: {device_id}\n"
                f"IP: {ip_address}\n"
                f"Firmware: {firmware}\n"
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
        
        # Try to locate devices with correct capitalization
        devices = None
        if "Devices" in system_status:
            devices = system_status.get("Devices", [])
        # Fallbacks for API inconsistency
        elif "devices" in system_status:
            devices = system_status.get("devices", [])
        elif "DEVICES" in system_status:
            devices = system_status.get("DEVICES", [])
        else:
            return "No 'Devices' field found in the API response."
        
        for device in devices:
            # Check for device ID with multiple possible field names
            device_unique_id = device.get("UniqueID") or device.get("uniqueID") or device.get("UNIQUE_ID") or ""
            
            if device_unique_id == device_id:
                # Handle different field name cases
                model = device.get("Model") or device.get("model") or device.get("MODEL") or "Unknown Model"
                name = device.get("Name") or device.get("name") or "Unnamed"
                ip_address = device.get("IpAddress") or device.get("ipAddress") or device.get("IP_ADDRESS") or "Not assigned"
                is_online = device.get("IsOnline", device.get("isOnline", device.get("IS_ONLINE", False)))
                is_linked = device.get("IsLinked", device.get("isLinked", device.get("IS_LINKED", False)))
                firmware = device.get("FirmwareVersion") or device.get("firmwareVersion") or device.get("FIRMWARE_VERSION") or "Unknown"
                serial = device.get("SerialNumber") or device.get("serialNumber") or device.get("SERIAL_NUMBER") or "Unknown"
                
                return (
                    f"Device Details:\n"
                    f"Name: {name}\n"
                    f"Model: {model}\n"
                    f"ID: {device_unique_id}\n"
                    f"IP: {ip_address}\n"
                    f"Status: {'Online' if is_online else 'Offline'}\n"
                    f"Linked: {'Yes' if is_linked else 'No'}\n"
                    f"Firmware: {firmware}\n"
                    f"Serial: {serial}"
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
        # Match payload format in check_armonia.py
        data = {
            "UniqueID": device_id,
            "Channel": str(channel),
            "Value": str(value)
        }
        response = call_armonia_api("SetAdvancedEqGain", method="POST", data=data, timeout=10)
        return f"Successfully set gain for device {device_id}, channel {channel} to {value}"
    except Exception as e:
        return f"Error setting device gain: {str(e)}"

@mcp.tool()
async def open_entity_details(device_id: str, entity_type: Optional[str] = None) -> str:
    """Open entity details for a specific device
    
    Args:
        device_id: The unique ID of the device
        entity_type: Optional entity type parameter
    """
    try:
        # According to API docs, only UniqueID is required
        payload = {
            "UniqueID": device_id
        }
        
        # Add EntityType only if provided (not in original API spec)
        if entity_type:
            payload["EntityType"] = entity_type
        
        # Use 100 second timeout as seen in check_armonia.py
        response = call_armonia_api("OpenEntityDetails", method="POST", data=payload, timeout=100)
        return f"Successfully opened entity details for device {device_id}"
    except Exception as e:
        return f"Error opening entity details: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio') 