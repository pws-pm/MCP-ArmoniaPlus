#!/usr/bin/env python3
"""
Simple script to check the ArmoníaPlus API connection
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Get API details from environment
    api_url = os.environ.get("ARMONIA_API_URL", "http://192.168.1.30:40402/api/ARA")
    auth_token = os.environ.get("ARMONIA_AUTH_TOKEN", "fcb0d2ee-9179-4968-8799-690fd242d530")
    
    print(f"Checking ArmoníaPlus API at {api_url}/GetSystemStatus...")
    
    try:
        # Make the API request
        response = requests.get(
            f"{api_url}/GetSystemStatus",
            headers={"authClientToken": auth_token},
            timeout=5
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            print("✅ ArmoníaPlus API is working!")
            
            # Parse the response
            data = response.json()
            devices = data.get("devices", [])
            
            if not devices:
                print("No devices found in the system.")
                return
            
            # Display the devices
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
                
        else:
            print(f"❌ API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to ArmoníaPlus API: {e}")
        print("Make sure ArmoníaPlus is running and the API is enabled.")

if __name__ == "__main__":
    main() 