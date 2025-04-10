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

@mcp.tool()
async def set_advanced_eq_delay(device_id: str, channel: int, value: float) -> str:
    """Set the delay of Advanced EQ for a specific device channel
    
    Args:
        device_id: The unique ID of the device
        channel: The channel number to adjust (0-based)
        value: The delay value to set (in milliseconds)
    """
    try:
        # Match payload format in check_armonia.py
        data = {
            "UniqueID": device_id,
            "Channel": str(channel),
            "Value": str(value)
        }
        response = call_armonia_api("SetAdvancedEqDelay", method="POST", data=data, timeout=10)
        return f"Successfully set delay for device {device_id}, channel {channel} to {value} ms"
    except Exception as e:
        return f"Error setting advanced EQ delay: {str(e)}"

@mcp.tool()
async def set_speaker_eq_fir(device_id: str, channel: int, values: List[float]) -> str:
    """Set the Speaker EQ FIR filters for a specific device channel
    
    Args:
        device_id: The unique ID of the device
        channel: The channel number to adjust (0-based)
        values: List of FIR coefficient values
    """
    try:
        # Convert values to strings as in check_armonia.py
        string_values = [str(val) for val in values]
        
        data = {
            "UniqueID": device_id,
            "Channel": str(channel),
            "Values": string_values
        }
        response = call_armonia_api("SetSpeakerEqFIR", method="POST", data=data, timeout=10)
        return f"Successfully set Speaker EQ FIR for device {device_id}, channel {channel} with {len(values)} coefficients"
    except Exception as e:
        return f"Error setting Speaker EQ FIR: {str(e)}"

@mcp.tool()
async def set_output_eq_fir(device_id: str, channel: int, values: List[float]) -> str:
    """Set the Output EQ FIR filters for a specific device channel
    
    Args:
        device_id: The unique ID of the device
        channel: The channel number to adjust (0-based)
        values: List of FIR coefficient values
    """
    try:
        # Convert values to strings as in check_armonia.py
        string_values = [str(val) for val in values]
        
        data = {
            "UniqueID": device_id,
            "Channel": str(channel),
            "Values": string_values
        }
        response = call_armonia_api("SetOutputEqFIR", method="POST", data=data, timeout=10)
        return f"Successfully set Output EQ FIR for device {device_id}, channel {channel} with {len(values)} coefficients"
    except Exception as e:
        return f"Error setting Output EQ FIR: {str(e)}"

@mcp.tool()
async def set_output_eq_gain(device_id: str, channel: int, value: float) -> str:
    """Set the Output EQ Gain for a specific device channel
    
    Args:
        device_id: The unique ID of the device
        channel: The channel number to adjust (0-based)
        value: The gain value to set (in dB)
    """
    try:
        data = {
            "UniqueID": device_id,
            "Channel": str(channel),
            "Value": str(value)
        }
        response = call_armonia_api("SetOutputEqGain", method="POST", data=data, timeout=10)
        return f"Successfully set Output EQ Gain for device {device_id}, channel {channel} to {value} dB"
    except Exception as e:
        return f"Error setting Output EQ Gain: {str(e)}"

@mcp.tool()
async def set_output_eq_phase(device_id: str, channel: int, invert_phase: bool) -> str:
    """Set the Output EQ Phase for a specific device channel
    
    Args:
        device_id: The unique ID of the device
        channel: The channel number to adjust (0-based)
        invert_phase: Whether to invert the phase (True) or set to normal (False)
    """
    try:
        data = {
            "UniqueID": device_id,
            "Channel": str(channel),
            "Value": invert_phase  # Boolean value as in check_armonia.py
        }
        response = call_armonia_api("SetOutputEqPhase", method="POST", data=data, timeout=10)
        phase_status = "inverted" if invert_phase else "normal"
        return f"Successfully set Output EQ Phase for device {device_id}, channel {channel} to {phase_status}"
    except Exception as e:
        return f"Error setting Output EQ Phase: {str(e)}"

@mcp.tool()
async def create_and_assign_group(group_links: List[Dict[str, str]]) -> str:
    """Create and assign a group with the specified links
    
    Args:
        group_links: List of dictionaries with UniqueID and Channel keys
        Example: [{"UniqueID": "device1_id", "Channel": "0"}, {"UniqueID": "device2_id", "Channel": "1"}]
    """
    try:
        data = {
            "GroupLinks": group_links
        }
        response = call_armonia_api("CreateAndAssignGroup", method="POST", data=data, timeout=10)
        
        # Extract group ID from response
        group_id = response.get("Guid", "Unknown")
        
        # Log successes and errors from response
        successes = response.get("Successes", {})
        errors = response.get("Errors", {})
        
        success_msg = f"Successfully created group with ID: {group_id}\n"
        
        if successes:
            success_msg += "Successful assignments:\n"
            for device_id, groups in successes.items():
                for group_id, channels in groups.items():
                    success_msg += f"- Device {device_id}, Group {group_id}: Channels {', '.join(channels)}\n"
        
        if errors:
            success_msg += "Failed assignments:\n"
            for error_info in errors:
                success_msg += f"- {error_info}\n"
                
        return success_msg
    except Exception as e:
        return f"Error creating and assigning group: {str(e)}"

@mcp.tool()
async def unassign_group(group_links: List[Dict[str, str]]) -> str:
    """Unassign channels from a group
    
    Args:
        group_links: List of dictionaries with UniqueID, Guid, and Channel keys
        Example: [{"UniqueID": "device1_id", "Guid": "group_guid", "Channel": "0"}]
    """
    try:
        # Verify each link has required fields
        for link in group_links:
            if "UniqueID" not in link or "Guid" not in link or "Channel" not in link:
                return f"Error: Each group link must contain 'UniqueID', 'Guid', and 'Channel' fields"
        
        data = {
            "GroupLinks": group_links
        }
        response = call_armonia_api("UnassignGroup", method="POST", data=data, timeout=10)
        
        # Log successes and errors from response
        successes = response.get("Successes", {})
        errors = response.get("Errors", {})
        
        success_msg = "Successfully unassigned from groups:\n"
        
        if successes:
            for device_id, groups in successes.items():
                for group_id, channels in groups.items():
                    success_msg += f"- Device {device_id}, Group {group_id}: Channels {', '.join(channels)}\n"
        
        if errors:
            success_msg += "Failed unassignments:\n"
            for error_info in errors:
                success_msg += f"- {error_info}\n"
                
        return success_msg
    except Exception as e:
        return f"Error unassigning from group: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio') 