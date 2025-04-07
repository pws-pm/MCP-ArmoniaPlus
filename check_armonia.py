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
    """Get the system status including all devices"""
    print("Getting system status...")
    
    try:
        response = requests.get(
            f"{api_url}/GetSystemStatus",
            headers={"authClientToken": auth_token},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ System status retrieved successfully!")
            data = response.json()
            if data.get("ERROR_CODE"):
                print(f"❌ API Error: {data.get('ERROR_CODE')}")
                print(f"Description: {data.get('ERROR_DESCRIPTION')}")
                return None
            
            # Process and display devices information
            devices = data.get("DEVICES", [])
            print(f"\nFound {len(devices)} devices:")
            
            for idx, device in enumerate(devices, 1):
                status = "🟢 ONLINE" if device.get("IS_ONLINE") else "🔴 OFFLINE"
                print(f"{idx}. {device.get('MODEL')} ({device.get('UNIQUE_ID')}) - {status}")
                
            return devices
        else:
            print(f"❌ Failed to get system status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to ArmoníaPlus API: {e}")
        return None

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
            data = response.json()
            if data.get("ERROR_CODE"):
                print(f"❌ API Error: {data.get('ERROR_CODE')}")
                print(f"Description: {data.get('ERROR_DESCRIPTION')}")
                return False
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
            data = response.json()
            if data.get("ERROR_CODE"):
                print(f"❌ API Error: {data.get('ERROR_CODE')}")
                print(f"Description: {data.get('ERROR_DESCRIPTION')}")
                return False
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
            data = response.json()
            if data.get("ERROR_CODE"):
                print(f"❌ API Error: {data.get('ERROR_CODE')}")
                print(f"Description: {data.get('ERROR_DESCRIPTION')}")
                return False
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
            data = response.json()
            if data.get("ERROR_CODE"):
                print(f"❌ API Error: {data.get('ERROR_CODE')}")
                print(f"Description: {data.get('ERROR_DESCRIPTION')}")
                return False
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
            data = response.json()
            if data.get("ERROR_CODE"):
                print(f"❌ API Error: {data.get('ERROR_CODE')}")
                print(f"Description: {data.get('ERROR_DESCRIPTION')}")
                return False
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
            data = response.json()
            if data.get("ERROR_CODE"):
                print(f"❌ API Error: {data.get('ERROR_CODE')}")
                print(f"Description: {data.get('ERROR_DESCRIPTION')}")
                return False
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

def open_entity_details(api_url, auth_token, unique_id, entity_type):
    """Open entity details for a specific device"""
    print(f"Opening entity details for device {unique_id}, type {entity_type}...")
    
    try:
        payload = {
            "UniqueID": unique_id,
            "EntityType": entity_type
        }
        
        response = requests.post(
            f"{api_url}/OpenEntityDetails",
            headers={"authClientToken": auth_token},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Entity details opened successfully!")
            data = response.json()
            if data.get("ERROR_CODE"):
                print(f"❌ API Error: {data.get('ERROR_CODE')}")
                print(f"Description: {data.get('ERROR_DESCRIPTION')}")
                return False
            
            print(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ Failed to open entity details: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to ArmoníaPlus API: {e}")
        return False

def select_device(devices):
    """Helper function to select a device from a list"""
    if not devices:
        print("No devices available.")
        return None
        
    print("\nSelect a device:")
    for idx, device in enumerate(devices, 1):
        status = "🟢 ONLINE" if device.get("IS_ONLINE") else "🔴 OFFLINE"
        print(f"{idx}. {device.get('MODEL')} ({device.get('UNIQUE_ID')}) - {status}")
        
    try:
        selection = int(input("\nEnter device number: ").strip())
        if 1 <= selection <= len(devices):
            return devices[selection - 1]
        else:
            print("❌ Invalid selection.")
            return None
    except ValueError:
        print("❌ Please enter a valid number.")
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
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description='Test ArmoníaPlus API connectivity and operations')
    parser.add_argument('--url', default='http://192.168.1.31:40402/api/ARA', 
                        help='ArmoníaPlus API URL (default: http://192.168.1.31:40402/api/ARA)')
    parser.add_argument('--token', default='fcb0d2ee-9179-4968-8799-690fd242d530',
                        help='Authentication token (default: fcb0d2ee-9179-4968-8799-690fd242d530)')
    args = parser.parse_args()
    
    print("=" * 60)
    print("ArmoníaPlus API Test Tool")
    print("=" * 60)
    print(f"API URL: {args.url}")
    print(f"Auth Token: {args.token}")
    print("=" * 60)
    
    # First, check if API is reachable
    devices = get_system_status(args.url, args.token)
    
    if not devices:
        print("❌ Could not retrieve devices. Please check the API URL and token.")
        return
    
    while True:
        print("\n" + "=" * 60)
        print("ArmoníaPlus API Operations Menu")
        print("=" * 60)
        print("1. Get System Status (List Devices)")
        print("2. Open Device Details")
        print("3. Set Advanced EQ Gain")
        print("4. Set Advanced EQ Delay")
        print("5. Set Advanced EQ Mode")
        print("6. Set Speaker EQ FIR")
        print("7. Set Output EQ FIR")
        print("8. Set Output EQ Gain")
        print("9. Set Output EQ Phase")
        print("0. Exit")
        print("=" * 60)
        
        choice = input("Select an operation (0-9): ").strip()
        
        if choice == '0':
            print("Exiting...")
            break
            
        elif choice == '1':
            devices = get_system_status(args.url, args.token)
            
        elif choice == '2':
            if devices:
                device = select_device(devices)
                if device:
                    # Ask for entity type
                    entity_type = input("Enter entity type (default: 'DEVICE'): ").strip() or "DEVICE"
                    open_entity_details(args.url, args.token, device.get('UNIQUE_ID'), entity_type)
            else:
                print("❌ No devices available. Please get system status first.")
                
        elif choice == '3':
            if devices:
                device = select_device(devices)
                if device:
                    channel = input("Enter channel number: ").strip()
                    try:
                        value = float(input("Enter gain value (dB): ").strip())
                        set_advanced_eq_gain(args.url, args.token, device.get('UNIQUE_ID'), channel, value)
                    except ValueError:
                        print("❌ Invalid gain value. Please enter a numeric value.")
            else:
                print("❌ No devices available. Please get system status first.")
                
        elif choice == '4':
            if devices:
                device = select_device(devices)
                if device:
                    channel = input("Enter channel number: ").strip()
                    try:
                        value = float(input("Enter delay value (ms): ").strip())
                        set_advanced_eq_delay(args.url, args.token, device.get('UNIQUE_ID'), channel, value)
                    except ValueError:
                        print("❌ Invalid delay value. Please enter a numeric value.")
            else:
                print("❌ No devices available. Please get system status first.")
                
        elif choice == '5':
            if devices:
                device = select_device(devices)
                if device:
                    channel = input("Enter channel number: ").strip()
                    eq_index = input("Enter EQ index: ").strip()
                    mode = input("Enter mode (e.g., 'PEAK', 'NOTCH', 'LOWSHELF', 'HIGHSHELF'): ").strip()
                    set_advanced_eq_mode(args.url, args.token, device.get('UNIQUE_ID'), channel, eq_index, mode)
            else:
                print("❌ No devices available. Please get system status first.")
                
        elif choice == '6':
            if devices:
                device = select_device(devices)
                if device:
                    channel = input("Enter channel number: ").strip()
                    values_str = input("Enter FIR values (comma separated): ").strip()
                    values = [v.strip() for v in values_str.split(',')]
                    set_speaker_eq_fir(args.url, args.token, device.get('UNIQUE_ID'), channel, values)
            else:
                print("❌ No devices available. Please get system status first.")
                
        elif choice == '7':
            if devices:
                device = select_device(devices)
                if device:
                    channel = input("Enter channel number: ").strip()
                    values_str = input("Enter FIR values (comma separated): ").strip()
                    values = [v.strip() for v in values_str.split(',')]
                    set_output_eq_fir(args.url, args.token, device.get('UNIQUE_ID'), channel, values)
            else:
                print("❌ No devices available. Please get system status first.")
                
        elif choice == '8':
            if devices:
                device = select_device(devices)
                if device:
                    channel = input("Enter channel number: ").strip()
                    try:
                        value = float(input("Enter gain value (dB): ").strip())
                        set_output_eq_gain(args.url, args.token, device.get('UNIQUE_ID'), channel, value)
                    except ValueError:
                        print("❌ Invalid gain value. Please enter a numeric value.")
            else:
                print("❌ No devices available. Please get system status first.")
                
        elif choice == '9':
            if devices:
                device = select_device(devices)
                if device:
                    channel = input("Enter channel number: ").strip()
                    phase_str = input("Enter phase (true/false): ").strip().lower()
                    if phase_str in ('true', 't', 'yes', 'y', '1'):
                        value = True
                    elif phase_str in ('false', 'f', 'no', 'n', '0'):
                        value = False
                    else:
                        print("❌ Invalid phase value. Please enter true or false.")
                        continue
                    set_output_eq_phase(args.url, args.token, device.get('UNIQUE_ID'), channel, value)
            else:
                print("❌ No devices available. Please get system status first.")
                
        else:
            print("❌ Invalid choice. Please try again.")
        
        # Pause before showing the menu again
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    sys.exit(main()) 