#!/usr/bin/env python3
"""
Wrapper script to run the MCP server with proper environment setup
"""

import os
import sys
import subprocess
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_environment():
    """Ensure the environment is properly set up"""
    # Check if required environment variables are set
    required_vars = {
        "ARMONIA_API_URL": os.environ.get("ARMONIA_API_URL", "http://localhost:40402/api/ARA"),
        "ARMONIA_AUTH_TOKEN": os.environ.get("ARMONIA_AUTH_TOKEN", "token-given-by-powersoft")
    }
    
    # Set variables if not already set
    for var, default in required_vars.items():
        if var not in os.environ:
            os.environ[var] = default
            print(f"Set {var}={default}")

def run_tests():
    """Run tests to verify the environment is ready for the MCP server"""
    print("Running environment tests...")
    
    # Try to import the required module
    try:
        import_cmd = [
            sys.executable, 
            "-c", 
            "import mcp; print(f'mcp found at {mcp.__file__}')"
        ]
        result = subprocess.run(import_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ MCP SDK is available")
            print(result.stdout.strip())
        else:
            print("❌ MCP SDK import failed")
            print(result.stderr.strip())
            return False
    except Exception as e:
        print(f"❌ Error checking MCP SDK: {e}")
        return False
    
    # Check mock API is running
    api_url = os.environ.get("ARMONIA_API_URL", "").rstrip("/")
    if not api_url:
        print("❌ ARMONIA_API_URL is not set")
        return False
    
    print(f"Checking ArmoníaPlus API at {api_url}/GetSystemStatus...")
    try:
        import requests
        response = requests.get(f"{api_url}/GetSystemStatus", 
                              headers={"authClientToken": os.environ.get("ARMONIA_AUTH_TOKEN", "")},
                              timeout=2)
        if response.status_code == 200:
            print("✅ ArmoníaPlus API is available")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ ArmoníaPlus API returned status code {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Error connecting to ArmoníaPlus API: {e}")
        print("   Make sure mock_armonia_api.py is running")
        return False
    
    return True

def run_server(use_simplified=False, host="0.0.0.0", port=8080):
    """Run the appropriate MCP server"""
    setup_environment()
    
    if use_simplified:
        print("Running simplified MCP server...")
        # Set environment variables for the simplified server
        os.environ["MCP_HOST"] = host
        os.environ["MCP_PORT"] = str(port)
        
        # Run the simplified server
        subprocess.run([sys.executable, "simplified_mcp_server.py"])
    else:
        print("Running official MCP server...")
        
        # Run pre-flight tests
        if not run_tests():
            print("\n⚠️ Environment tests failed. You have two options:")
            print("1. Fix the issues described above and try again")
            print("2. Run with --simplified flag to use the simplified server")
            return
        
        # Run the official MCP server
        subprocess.run([sys.executable, "mcp_server_armonia.py"])

def main():
    parser = argparse.ArgumentParser(description="Run the MCP server for ArmoníaPlus")
    parser.add_argument("--simplified", "-s", action="store_true", 
                       help="Use the simplified MCP server (no SDK required)")
    parser.add_argument("--host", type=str, default="0.0.0.0",
                       help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8080,
                       help="Port to run the server on")
    args = parser.parse_args()
    
    run_server(use_simplified=args.simplified, host=args.host, port=args.port)

if __name__ == "__main__":
    main() 