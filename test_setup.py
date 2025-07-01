#!/usr/bin/env python3
"""
Test setup for Trad-Chem LLM
Verifies all components are properly configured

@author Anu Gamage
LinkedIn: https://www.linkedin.com/in/anu-gamage-62192b201/
"""

import os
import sys

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("🧪 Testing Dependencies...")
    
    required_packages = [
        'streamlit',
        'google.generativeai',
        'requests',
        'pandas',
        'numpy',
        'jsonschema'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 Trad-Chem LLM Setup Test")
    print("=" * 40)
    
    success = test_dependencies()
    
    if success:
        print("\n🎉 All tests passed! Your setup is ready.")
    else:
        print("\n💥 Some tests failed. Please install missing dependencies.")
    
    sys.exit(0 if success else 1) 