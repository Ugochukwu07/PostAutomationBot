#!/usr/bin/env python3
"""
Test script for RecentHPost API integration
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_client import APIClient
from config import Config

def test_api_connection():
    """Test the API connection and make a test post"""
    print("🔍 Testing RecentHPost API Connection...")
    
    # Load environment variables
    load_dotenv()
    
    # Validate configuration
    try:
        Config.validate_config()
        print("✅ Configuration validated")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return False
    
    # Test API connection
    api_client = APIClient()
    
    print(f"📡 Testing connection to: {Config.API_ENDPOINT}")
    print(f"🔑 Using API key: {Config.API_KEY[:10]}...")
    
    if api_client.test_connection():
        print("✅ API connection test successful!")
        return True
    else:
        print("❌ API connection test failed!")
        return False

def test_single_post():
    """Test making a single post"""
    print("\n📝 Testing single post...")
    
    api_client = APIClient()
    
    test_content = "This is a test post from the Automated Poster Bot! 🤖"
    test_title = "API Test Post"
    test_hashtags = ["#test", "#bot", "#autopost"]
    
    result = api_client.post_content(
        content=test_content,
        title=test_title,
        hashtags=test_hashtags
    )
    
    if result['success']:
        print("✅ Test post successful!")
        print(f"📊 Status Code: {result['status_code']}")
        if result.get('response'):
            print(f"📄 Response: {result['response']}")
        return True
    else:
        print("❌ Test post failed!")
        print(f"🚨 Error: {result.get('error', 'Unknown error')}")
        print(f"📊 Status Code: {result.get('status_code', 'N/A')}")
        return False

def main():
    """Main test function"""
    print("🚀 RecentHPost API Integration Test")
    print("=" * 50)
    
    # Test 1: Configuration
    print("\n1️⃣ Testing Configuration...")
    try:
        Config.validate_config()
        print("✅ Configuration is valid")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("💡 Make sure to copy env_example.txt to .env and fill in your values")
        return
    
    # Test 2: API Connection
    print("\n2️⃣ Testing API Connection...")
    if not test_api_connection():
        print("💡 Check your API endpoint and key in the .env file")
        return
    
    # Test 3: Single Post
    print("\n3️⃣ Testing Single Post...")
    if not test_single_post():
        print("💡 Check the API endpoint and your network connection")
        return
    
    print("\n🎉 All tests passed! Your API integration is working correctly.")
    print("💡 You can now run the main bot with: python main.py")

if __name__ == "__main__":
    main() 