#!/usr/bin/env python3
"""
Test script for Automated Daily Poster Bot
Tests individual components without requiring actual API endpoints
"""

import os
import sys
import logging
from unittest.mock import Mock, patch
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from content_fetcher import ContentFetcher
from database import DatabaseManager
from scheduler import PostScheduler

def test_content_fetcher():
    """Test content fetcher with mock APIs"""
    print("🧪 Testing Content Fetcher...")
    
    fetcher = ContentFetcher()
    
    # Test fallback content
    fallback = fetcher.get_fallback_content()
    assert 'content' in fallback
    assert 'api_name' in fallback
    assert fallback['api_name'] == 'Fallback'
    print("✅ Fallback content works")
    
    # Test with mock API response
    with patch('requests.Session.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {
            'content': 'Test quote',
            'author': 'Test Author'
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Mock random.choice to return a specific API
        with patch('random.choice') as mock_choice:
            mock_choice.return_value = {
                'name': 'Quotes API',
                'url': 'https://api.quotable.io/random',
                'content_key': 'content',
                'author_key': 'author'
            }
            
            content_data = fetcher.fetch_content()
            assert 'content' in content_data
            assert 'api_name' in content_data
            print("✅ Mock API content fetching works")
    
    print("✅ Content Fetcher tests passed\n")

def test_database_manager():
    """Test database manager with mock connection"""
    print("🧪 Testing Database Manager...")
    
    db_manager = DatabaseManager()
    
    # Test without actual connection
    with patch('mysql.connector.connect') as mock_connect:
        mock_connection = Mock()
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection
        
        # Test connection
        result = db_manager.connect()
        assert result == True
        print("✅ Database connection test passed")
        
        # Test table creation
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        db_manager.create_tables()
        mock_cursor.execute.assert_called()
        print("✅ Table creation test passed")
        
        # Test post logging
        db_manager.log_post('TEST', 'SUCCESS', 'Test API', 'Test content')
        mock_cursor.execute.assert_called()
        print("✅ Post logging test passed")
    
    print("✅ Database Manager tests passed\n")

def test_scheduler():
    """Test scheduler logic"""
    print("🧪 Testing Post Scheduler...")
    
    # Mock database manager
    mock_db = Mock()
    mock_db.get_today_posts_count.return_value = 2
    mock_db.get_today_posts_count.side_effect = lambda post_type=None: 1 if post_type == 'RANDOM' else 2
    
    scheduler = PostScheduler(mock_db)
    
    # Test remaining posts calculation
    remaining = scheduler.calculate_remaining_posts()
    assert remaining == 4  # 5 - 1 = 4
    print("✅ Remaining posts calculation works")
    
    # Test time remaining calculation
    time_remaining = scheduler.calculate_time_remaining_today()
    assert time_remaining > 0
    print("✅ Time remaining calculation works")
    
    # Test post distribution
    post_times = scheduler.distribute_posts_intelligently(3, 5.0)  # 3 posts over 5 hours
    assert len(post_times) == 3
    print("✅ Post distribution works")
    
    print("✅ Post Scheduler tests passed\n")

def test_config():
    """Test configuration validation"""
    print("🧪 Testing Configuration...")
    
    # Test with missing required fields
    original_endpoint = Config.API_ENDPOINT
    Config.API_ENDPOINT = ""
    
    try:
        Config.validate_config()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Missing required configuration" in str(e)
        print("✅ Configuration validation works")
    
    # Restore original values
    Config.API_ENDPOINT = original_endpoint
    
    print("✅ Configuration tests passed\n")

def test_content_apis():
    """Test content API configurations"""
    print("🧪 Testing Content APIs...")
    
    apis = Config.CONTENT_APIS
    assert len(apis) > 0
    print(f"✅ Found {len(apis)} content APIs")
    
    for api in apis:
        assert 'name' in api
        assert 'url' in api
        assert 'content_key' in api
        print(f"✅ API '{api['name']}' configuration valid")
    
    print("✅ Content APIs tests passed\n")

def main():
    """Run all tests"""
    print("🚀 Starting Automated Poster Bot Tests...\n")
    
    # Disable logging for tests
    logging.disable(logging.CRITICAL)
    
    try:
        test_config()
        test_content_apis()
        test_content_fetcher()
        test_database_manager()
        test_scheduler()
        
        print("🎉 All tests passed! The bot components are working correctly.")
        print("\n📝 Next steps:")
        print("1. Set up your .env file with real API endpoints")
        print("2. Configure your MySQL database")
        print("3. Run: python main.py --test")
        print("4. Start the bot: python main.py")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 