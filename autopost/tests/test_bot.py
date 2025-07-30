#!/usr/bin/env python3
"""
Test script for the Automated Poster Bot
Tests basic functionality and API connections
"""

import sys
import os
import time
from datetime import datetime

# Add the parent directory to the path to import the autopost package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from autopost.core.bot import AutomatedPosterBot
from autopost.config.settings import Config


def test_bot_initialization():
    """Test bot initialization"""
    print("🧪 Testing bot initialization...")

    try:
        bot = AutomatedPosterBot()
        print("✅ Bot instance created successfully")

        # Test initialization
        if bot.initialize():
            print("✅ Bot initialization successful")
            return True
        else:
            print("❌ Bot initialization failed")
            return False

    except Exception as e:
        print(f"❌ Bot initialization error: {e}")
        return False


def test_api_connection():
    """Test API connection"""
    print("\n🧪 Testing API connection...")

    try:
        bot = AutomatedPosterBot()

        if bot.api_client.test_connection():
            print("✅ API connection successful")
            return True
        else:
            print("❌ API connection failed")
            return False

    except Exception as e:
        print(f"❌ API connection error: {e}")
        return False


def test_content_fetching():
    """Test content fetching from APIs"""
    print("\n🧪 Testing content fetching...")

    try:
        bot = AutomatedPosterBot()

        # Test content fetching
        content_data = bot.content_fetcher.fetch_content()

        if content_data and "content" in content_data:
            print("✅ Content fetching successful")
            print(f"   Source: {content_data.get('api_name', 'Unknown')}")
            print(f"   Content: {content_data['content'][:100]}...")
            return True
        else:
            print("❌ Content fetching failed")
            return False

    except Exception as e:
        print(f"❌ Content fetching error: {e}")
        return False


def test_database_connection():
    """Test database connection"""
    print("\n🧪 Testing database connection...")

    try:
        bot = AutomatedPosterBot()

        if bot.database_manager.connect():
            print("✅ Database connection successful")

            # Test table creation
            bot.database_manager.create_tables()
            print("✅ Database tables created/verified")

            return True
        else:
            print("❌ Database connection failed")
            return False

    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False


def test_test_post():
    """Test making a test post"""
    print("\n🧪 Testing test post...")

    try:
        bot = AutomatedPosterBot()

        if bot.initialize():
            success = bot.make_test_post()

            if success:
                print("✅ Test post successful")
                return True
            else:
                print("❌ Test post failed")
                return False
        else:
            print("❌ Bot initialization failed for test post")
            return False

    except Exception as e:
        print(f"❌ Test post error: {e}")
        return False


def test_bot_status():
    """Test bot status functionality"""
    print("\n🧪 Testing bot status...")

    try:
        bot = AutomatedPosterBot()

        if bot.initialize():
            status = bot.get_status()

            print("✅ Bot status retrieved successfully")
            print(f"   Running: {status.get('is_running', False)}")
            print(f"   Posts Today: {status.get('posts_today', 0)}")
            print(f"   Random Posts: {status.get('random_posts_today', 0)}")
            print(f"   Scheduled Posts: {status.get('scheduled_posts_today', 0)}")

            return True
        else:
            print("❌ Bot initialization failed for status check")
            return False

    except Exception as e:
        print(f"❌ Bot status error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Automated Poster Bot Tests")
    print("=" * 50)

    tests = [
        ("Bot Initialization", test_bot_initialization),
        ("API Connection", test_api_connection),
        ("Content Fetching", test_content_fetching),
        ("Database Connection", test_database_connection),
        ("Bot Status", test_bot_status),
        ("Test Post", test_test_post),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 30)

        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Bot is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check configuration and connections.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
