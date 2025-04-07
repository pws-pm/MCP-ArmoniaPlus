#!/usr/bin/env python3
"""
Comprehensive ArmoníaPlus API testing tool

This script provides a command-line interface to test all supported
API endpoints of the ArmoníaPlus system.

Based on API-Armonia.md documentation.
"""

import os
import sys
import json
import argparse
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
DEFAULT_API_URL = "http://192.168.1.30:40402/api/ARA"
DEFAULT_AUTH_TOKEN = "fcb0d2ee-9179-4968-8799-690fd242d530"

def get_system_status(api_url, auth_token):
    """Get the status of all devices in the ArmoníaPlus system"""
    print(f"Checking ArmoníaPlus API at {api_url}/GetSystemStatus...")
    
    try:
        response = requests.get(
            f"{api_url}/GetSystemStatus",
            headers={"authClientToken": auth_token},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ ArmoníaPlus API is working!")
            data = response.json()
            devices = data.get("devices", [])
            
            if not devices:
                print("No devices found in the system.")
                return []
            
            print(f"\nFound {len(devices)} devices:")
            print("-" * 50)
            
            for i, device in enumerate(devices, 1):
                name = device.get("name", "Unnamed")
                model = device.get("model", "Unknown")
                status = "Online" if device.get("isOnline", False) else "Offline"
                device_id = device.get("uniqueID", "Unknown")
                
                print(f"{i}. {name} ({model}) - {status}")
                print(f"   ID: {device_id}")
                print()
                
            return devices
        else:
            print(f"❌ API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to ArmoníaPlus API: {e}")
        print("Make sure ArmoníaPlus is running and the API is enabled.")
        return []

def set_advanced_eq_gain(api_url, auth_token, unique_id, channel, value):
    """Set the gain of Advanced EQ for a specific channel"""
    print(f"Setting Advanced EQ Gain for device {unique_id}, channel {channel} to {value}...")
    
    try:
        payload = {
            "UniqueID": unique_id,
            "Channel": str(channel),
            "Value": str(value)
        }
        
        response = requests.post(
            f"{api_url}/SetAdvancedEqGain",
            headers={"authClientToken": auth_token},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Advanced EQ Gain set successfully!")
            return True
        else:
            print(f"❌ Failed to set Advanced EQ Gain: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to ArmoníaPlus API: {e}")
        return False

def set_advanced_eq_delay(api_url, auth_token, unique_id, channel, value):
    """Set the delay of Advanced EQ for a specific channel"""
    print(f"Setting Advanced EQ Delay for device {unique_id}, channel {channel} to {value}...")
    
    try:
        payload = {
            "UniqueID": unique_id,
            "Channel": str(channel),
            "Value": str(value)
        }
        
        response = requests.post(
            f"{api_url}/SetAdvancedEqDelay",
            headers={"authClientToken": auth_token},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Advanced EQ Delay set successfully!")
            return True
        else:
            print(f"❌ Failed to set Advanced EQ Delay: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to ArmoníaPlus API: {e}")
        return False

def set_speaker_eq_fir(api_url, auth_token, unique_id, channel, values):
    """Set the Speaker EQ FIR for a specific channel"""
    print(f"Setting Speaker EQ FIR for device {unique_id}, channel {channel}...")
    
    try:
        # Convert numeric values to strings if necessary
        string_values = [str(val) for val in values]
        
        payload = {
            "UniqueID": unique_id,
            "Channel": str(channel),
            "Values": string_values
        }
        
        response = requests.post(
            f"{api_url}/SetSpeakerEqFIR",
            headers={"authClientToken": auth_token},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Speaker EQ FIR set successfully!")
            return True
        else:
            print(f"❌ Failed to set Speaker EQ FIR: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to ArmoníaPlus API: {e}")
        return False

def set_output_eq_fir(api_url, auth_token, unique_id, channel, values):
    """Set the Output EQ FIR for a specific channel"""
    print(f"Setting Output EQ FIR for device {unique_id}, channel {channel}...")
    
    try:
        # Convert numeric values to strings if necessary
        string_values = [str(val) for val in values]
        
        payload = {
            "UniqueID": unique_id,
            "Channel": str(channel),
            "Values": string_values
        }
        
        response = requests.post(
            f"{api_url}/SetOutputEqFIR",
            headers={"authClientToken": auth_token},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Output EQ FIR set successfully!")
            return True
        else:
            print(f"❌ Failed to set Output EQ FIR: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to ArmoníaPlus API: {e}")
        return False

def set_output_eq_gain(api_url, auth_token, unique_id, channel, value):
    """Set the Output EQ Gain for a specific channel"""
    print(f"Setting Output EQ Gain for device {unique_id}, channel {channel} to {value}...")
    
    try:
        payload = {
            "UniqueID": unique_id,
            "Channel": str(channel),
            "Value": str(value)
        }
        
        response = requests.post(
            f"{api_url}/SetOutputEqGain",
            headers={"authClientToken": auth_token},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Output EQ Gain set successfully!")
            return True
        else:
            print(f"❌ Failed to set Output EQ Gain: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to ArmoníaPlus API: {e}")
        return False

def set_output_eq_phase(api_url, auth_token, unique_id, channel, value):
    """Set the Output EQ Phase for a specific channel"""
    print(f"Setting Output EQ Phase for device {unique_id}, channel {channel} to {value}...")
    
    try:
        payload = {
            "UniqueID": unique_id,
            "Channel": str(channel),
            "Value": value  # Boolean value
        }
        
        response = requests.post(
            f"{api_url}/SetOutputEqPhase",
            headers={"authClientToken": auth_token},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Output EQ Phase set successfully!")
            return True
        else:
            print(f"❌ Failed to set Output EQ Phase: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to ArmoníaPlus API: {e}")
        return False

def create_and_assign_group(api_url, auth_token, group_links):
    """Create and assign a group with the specified links"""
    print(f"Creating and assigning group with {len(group_links)} links...")
    
    try:
        payload = {
            "GroupLinks": group_links
        }
        
        response = requests.post(
            f"{api_url}/CreateAndAssignGroup",
            headers={"authClientToken": auth_token},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Group created and assigned successfully!")
            data = response.json()
            group_id = data.get("Guid")
            print(f"Group ID: {group_id}")
            return data
        else:
            print(f"❌ Failed to create and assign group: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to ArmoníaPlus API: {e}")
        return None

def unassign_group(api_url, auth_token, group_links):
    """Unassign a group with the specified links"""
    print(f"Unassigning group with {len(group_links)} links...")
    
    try:
        payload = {
            "GroupLinks": group_links
        }
        
        response = requests.post(
            f"{api_url}/UnassignGroup",
            headers={"authClientToken": auth_token},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Group unassigned successfully!")
            return True
        else:
            print(f"❌ Failed to unassign group: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to ArmoníaPlus API: {e}")
        return False

def open_entity_details(api_url, auth_token, unique_id):
    """Open and view the entity details"""
    print(f"Opening entity details for device {unique_id}...")
    
    try:
        payload = {
            "UniqueID": unique_id
        }
        
        response = requests.post(
            f"{api_url}/OpenEntityDetails",
            headers={"authClientToken": auth_token},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Entity details opened successfully!")
            return True
        else:
            print(f"❌ Failed to open entity details: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to ArmoníaPlus API: {e}")
        return False

def select_device(devices):
    """Interactive selection of a device from the list"""
    if not devices:
        print("No devices available to select.")
        return None
        
    print("\nSelect a device:")
    for i, device in enumerate(devices, 1):
        name = device.get("name", "Unnamed")
        model = device.get("model", "Unknown")
        status = "Online" if device.get("isOnline", False) else "Offline"
        print(f"{i}. {name} ({model}) - {status}")
    
    choice = input("\nEnter device number (or 0 to cancel): ")
    try:
        index = int(choice) - 1
        if index == -1:
            return None
        if 0 <= index < len(devices):
            return devices[index]
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def select_channel(max_channels=8):
    """Interactive selection of a channel"""
    print("\nSelect a channel:")
    for i in range(max_channels):
        print(f"{i}. Channel {i}")
    
    choice = input("\nEnter channel number (or x to cancel): ")
    if choice.lower() == 'x':
        return None
    
    try:
        channel = int(choice)
        if 0 <= channel < max_channels:
            return channel
        else:
            print("Invalid channel number.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def get_float_value(prompt, min_val=-float('inf'), max_val=float('inf')):
    """Get a float value from user input with range validation"""
    while True:
        try:
            value_str = input(prompt)
            if value_str.lower() == 'x':
                return None
            
            value = float(value_str)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Value must be between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_boolean_value(prompt):
    """Get a boolean value from user input"""
    while True:
        choice = input(f"{prompt} (y/n or x to cancel): ").lower()
        if choice == 'x':
            return None
        elif choice in ('y', 'yes', 'true', '1'):
            return True
        elif choice in ('n', 'no', 'false', '0'):
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def get_fir_values():
    """Get FIR filter values from user input"""
    print("\nEnter FIR filter values (comma-separated list of numbers, or 'x' to cancel):")
    print("Example: 0.125,0.230,0.314,0.374,-0.412,0.428,0.424")
    
    values_str = input("> ")
    if values_str.lower() == 'x':
        return None
    
    try:
        # Split by comma and convert to float
        values = [float(v.strip()) for v in values_str.split(',')]
        if not values:
            print("No values provided.")
            return None
        return values
    except ValueError:
        print("Invalid input. Please enter comma-separated numbers.")
        return None

def create_group_links():
    """Create group links from user input"""
    links = []
    while True:
        print("\nEnter group link details (or 'x' to finish):")
        device_id = input("Device ID (or 'x' to finish): ")
        if device_id.lower() == 'x':
            break
            
        channel = input("Channel: ")
        try:
            channel_num = int(channel)
            links.append({
                "UniqueID": device_id,
                "Channel": str(channel_num)
            })
            print(f"Added link for device {device_id}, channel {channel_num}")
        except ValueError:
            print("Invalid channel number.")
    
    return links

def main():
    """Main function to run the ArmoníaPlus API testing tool"""
    parser = argparse.ArgumentParser(description='ArmoníaPlus API Testing Tool')
    parser.add_argument('--url', help='ArmoníaPlus API URL', 
                        default=os.environ.get("ARMONIA_API_URL", DEFAULT_API_URL))
    parser.add_argument('--token', help='Authentication token', 
                        default=os.environ.get("ARMONIA_AUTH_TOKEN", DEFAULT_AUTH_TOKEN))
    args = parser.parse_args()
    
    api_url = args.url
    auth_token = args.token
    
    print("="*50)
    print("ArmoníaPlus API Testing Tool")
    print("="*50)
    print(f"API URL: {api_url}")
    print("="*50)
    
    # First check if the API is accessible
    devices = get_system_status(api_url, auth_token)
    if not devices:
        print("Cannot proceed without accessible devices.")
        return 1
    
    while True:
        print("\n" + "="*50)
        print("Select an API command to test:")
        print("1. GetSystemStatus - Refresh device list")
        print("2. SetAdvancedEqGain - Set the gain of Advanced EQ")
        print("3. SetAdvancedEqDelay - Set the delay of Advanced EQ")
        print("4. SetSpeakerEqFIR - Set the Speaker EQ FIR")
        print("5. SetOutputEqFIR - Set the Output EQ FIR")
        print("6. SetOutputEqGain - Set the Output EQ Gain")
        print("7. SetOutputEqPhase - Set the Output EQ Phase")
        print("8. CreateAndAssignGroup - Create and assign a group")
        print("9. UnassignGroup - Unassign a group")
        print("10. OpenEntityDetails - Open entity details")
        print("0. Exit")
        print("="*50)
        
        choice = input("\nEnter your choice (0-10): ")
        
        if choice == '0':
            print("Exiting...")
            break
            
        elif choice == '1':
            devices = get_system_status(api_url, auth_token)
            
        elif choice == '2':
            device = select_device(devices)
            if device:
                channel = select_channel()
                if channel is not None:
                    value = get_float_value("Enter gain value (-80 to 20 dB, or 'x' to cancel): ", -80, 20)
                    if value is not None:
                        set_advanced_eq_gain(api_url, auth_token, device['uniqueID'], channel, value)
                        
        elif choice == '3':
            device = select_device(devices)
            if device:
                channel = select_channel()
                if channel is not None:
                    value = get_float_value("Enter delay value (0 to 2000 ms, or 'x' to cancel): ", 0, 2000)
                    if value is not None:
                        set_advanced_eq_delay(api_url, auth_token, device['uniqueID'], channel, value)
                        
        elif choice == '4':
            device = select_device(devices)
            if device:
                channel = select_channel()
                if channel is not None:
                    values = get_fir_values()
                    if values:
                        set_speaker_eq_fir(api_url, auth_token, device['uniqueID'], channel, values)
                        
        elif choice == '5':
            device = select_device(devices)
            if device:
                channel = select_channel()
                if channel is not None:
                    values = get_fir_values()
                    if values:
                        set_output_eq_fir(api_url, auth_token, device['uniqueID'], channel, values)
                        
        elif choice == '6':
            device = select_device(devices)
            if device:
                channel = select_channel()
                if channel is not None:
                    value = get_float_value("Enter gain value (-80 to 20 dB, or 'x' to cancel): ", -80, 20)
                    if value is not None:
                        set_output_eq_gain(api_url, auth_token, device['uniqueID'], channel, value)
                        
        elif choice == '7':
            device = select_device(devices)
            if device:
                channel = select_channel()
                if channel is not None:
                    value = get_boolean_value("Invert phase?")
                    if value is not None:
                        set_output_eq_phase(api_url, auth_token, device['uniqueID'], channel, value)
                        
        elif choice == '8':
            group_links = create_group_links()
            if group_links:
                create_and_assign_group(api_url, auth_token, group_links)
                
        elif choice == '9':
            group_links = create_group_links()
            if group_links:
                unassign_group(api_url, auth_token, group_links)
                
        elif choice == '10':
            device = select_device(devices)
            if device:
                open_entity_details(api_url, auth_token, device['uniqueID'])
                
        else:
            print("Invalid choice. Please try again.")
            
    return 0

if __name__ == "__main__":
    sys.exit(main()) 