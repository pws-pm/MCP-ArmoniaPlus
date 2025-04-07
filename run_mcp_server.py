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

def print_stderr(*args, **kwargs):
    """Print to stderr instead of stdout"""
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)

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
            print_stderr(f"Set {var}={default}")

def run_tests():
    """Run tests to verify the environment is ready for the MCP server"""
    print_stderr("Running environment tests...")
    
    # Try to import the required module
    try:
        import_cmd = [
            sys.executable, 
            "-c", 
            "import mcp; print(f'mcp found at {mcp.__file__}')"
        ]
        result = subprocess.run(import_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_stderr("✅ MCP SDK is available")
            print_stderr(result.stdout.strip())
        else:
            print_stderr("❌ MCP SDK import failed")
            print_stderr(result.stderr.strip())
            return False
    except Exception as e:
        print_stderr(f"❌ Error checking MCP SDK: {e}")
        return False
    
    # Check mock API is running
    api_url = os.environ.get("ARMONIA_API_URL", "").rstrip("/")
    if not api_url:
        print_stderr("❌ ARMONIA_API_URL is not set")
        return False
    
    print_stderr(f"Checking ArmoníaPlus API at {api_url}/GetSystemStatus...")
    try:
        import requests
        response = requests.get(f"{api_url}/GetSystemStatus", 
                              headers={"authClientToken": os.environ.get("ARMONIA_AUTH_TOKEN", "")},
                              timeout=10)
        if response.status_code == 200:
            print_stderr("✅ ArmoníaPlus API is available")
            print_stderr(f"Response: {response.json()}")
        else:
            print_stderr(f"❌ ArmoníaPlus API returned status code {response.status_code}")
            return False
    except requests.RequestException as e:
        print_stderr(f"❌ Error connecting to ArmoníaPlus API: {e}")
        print_stderr("   Make sure the ArmoníaPlus software is running with ARA API enabled")
        return False
    
    return True

def run_server(use_simplified=False, host="0.0.0.0", port=8080, skip_checks=False):
    """Run the appropriate MCP server"""
    setup_environment()
    
    if use_simplified:
        print_stderr("Running simplified MCP server...")
        # Set environment variables for the simplified server
        os.environ["MCP_HOST"] = host
        os.environ["MCP_PORT"] = str(port)
        
        # Run the simplified server
        subprocess.run([sys.executable, "simplified_mcp_server.py"])
    else:
        print_stderr("Running official MCP server...")
        
        # Run pre-flight tests if not skipped
        if not skip_checks and not run_tests():
            print_stderr("\n⚠️ Environment tests failed. You have two options:")
            print_stderr("1. Fix the issues described above and try again")
            print_stderr("2. Run with --no-check flag to bypass connectivity tests")
            return
        
        # Run the official MCP server
        os.execv(sys.executable, [sys.executable, "mcp_server_armonia.py"])

def main():
    parser = argparse.ArgumentParser(description="Run the MCP server for ArmoníaPlus")
    parser.add_argument("--simplified", "-s", action="store_true", 
                       help="Use the simplified MCP server (no SDK required)")
    parser.add_argument("--host", type=str, default="0.0.0.0",
                       help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8080,
                       help="Port to run the server on")
    parser.add_argument("--no-check", action="store_true",
                       help="Skip connectivity checks")
    args = parser.parse_args()
    
    run_server(use_simplified=args.simplified, host=args.host, port=args.port, skip_checks=args.no_check)

if __name__ == "__main__":
    main() 