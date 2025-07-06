#!/usr/bin/env python3
"""
Script to run all medium-level APIs simultaneously
"""

import subprocess
import time
import sys
import os
from threading import Thread

def run_api(api_name, port, filename):
    """Run a single API in a separate thread"""
    try:
        print(f"🚀 Starting {api_name} on port {port}...")
        subprocess.run([sys.executable, filename], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {api_name}: {e}")
    except KeyboardInterrupt:
        print(f"⏹️  Stopping {api_name}...")

def main():
    """Main function to run all APIs"""
    
    # API configurations
    apis = [
        {
            'name': 'User Management API',
            'port': 5001,
            'file': 'user_management_api.py'
        },
        {
            'name': 'E-commerce API',
            'port': 5002,
            'file': 'ecommerce_api.py'
        },
        {
            'name': 'Blog API',
            'port': 5003,
            'file': 'blog_api.py'
        },
        {
            'name': 'Task Management API',
            'port': 5004,
            'file': 'task_management_api.py'
        },
        {
            'name': 'Weather API',
            'port': 5005,
            'file': 'weather_api.py'
        }
    ]
    
    print("🌟 Starting Medium-Level Flask APIs...")
    print("=" * 50)
    
    # Check if all API files exist
    missing_files = []
    for api in apis:
        if not os.path.exists(api['file']):
            missing_files.append(api['file'])
    
    if missing_files:
        print(f"❌ Missing API files: {', '.join(missing_files)}")
        print("Please make sure all API files are in the current directory.")
        return
    
    # Start all APIs in separate threads
    threads = []
    for api in apis:
        thread = Thread(target=run_api, args=(api['name'], api['port'], api['file']))
        thread.daemon = True
        thread.start()
        threads.append(thread)
        time.sleep(1)  # Small delay between starts
    
    print("\n✅ All APIs are starting up...")
    print("\n📋 API Endpoints:")
    print("-" * 30)
    for api in apis:
        print(f"🌐 {api['name']}: http://localhost:{api['port']}")
    
    print("\n📚 Documentation: README.md")
    print("🛑 Press Ctrl+C to stop all APIs")
    print("=" * 50)
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down all APIs...")
        print("Thanks for using Medium-Level Flask APIs! 👋")

if __name__ == "__main__":
    main() 