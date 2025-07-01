#!/usr/bin/env python3
"""
Trad-Chem LLM Launcher Script
@author SaltyHeart

This script launches the Trad-Chem LLM Streamlit application.
Run this script to start the chatbot server.
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import streamlit
        import google.generativeai
        import dotenv
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("⚠️ .env file not found")
        print("Please copy .env.template to .env and configure your API keys")
        return False
    return True

def main():
    """Main launcher function"""
    print("🧪 Starting Trad-Chem LLM...")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment setup
    check_env_file()
    
    # Launch Streamlit app
    print("🚀 Launching Streamlit application...")
    try:
        subprocess.run([
            sys.executable, 
            "-m", "streamlit", 
            "run", 
            "app.py",
            "--server.port=8501",
            "--server.address=localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down Trad-Chem LLM...")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 