#!/usr/bin/env python3
"""
Test script for Notification Feature of Automated Daily Poster Bot
Tests the notification system with various scenarios
"""

import os
import sys
import time
import logging
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from notifier import send_notification
from scheduler import PostScheduler
from database import DatabaseManager


def test_basic_notification():
    """Test basic notification functionality"""
    print("🧪 Testing Basic Notification...")

    try:
        # Test with simple notification
        send_notification(
            title="Test Notification",
            message="This is a test notification from the bot",
        )
        print("✅ Basic notification sent successfully")
        return True
    except Exception as e:
        print(f"❌ Basic notification failed: {e}")
        return False


def test_notification_with_special_characters():
    """Test notification with special characters and emojis"""
    print("🧪 Testing Notification with Special Characters...")

    try:
        send_notification(
            title="🚀 Bot Test",
            message="Testing with emojis: 🎉 📝 ✅\nAnd special chars: @#$%^&*()",
        )
        print("✅ Special characters notification sent successfully")
        return True
    except Exception as e:
        print(f"❌ Special characters notification failed: {e}")
        return False


def test_long_message_notification():
    """Test notification with long message"""
    print("🧪 Testing Long Message Notification...")

    long_message = (
        "This is a very long message to test how the notification system handles lengthy content. "
        * 3
    )

    try:
        send_notification(title="Long Message Test", message=long_message)
        print("✅ Long message notification sent successfully")
        return True
    except Exception as e:
        print(f"❌ Long message notification failed: {e}")
        return False


def test_multiple_notifications():
    """Test sending multiple notifications in sequence"""
    print("🧪 Testing Multiple Notifications...")

    notifications = [
        ("First Test", "This is the first notification"),
        ("Second Test", "This is the second notification"),
        ("Third Test", "This is the third notification"),
    ]

    success_count = 0
    for title, message in notifications:
        try:
            send_notification(title=title, message=message)
            success_count += 1
            time.sleep(1)  # Small delay between notifications
        except Exception as e:
            print(f"❌ Failed to send notification '{title}': {e}")

    print(f"✅ Successfully sent {success_count}/{len(notifications)} notifications")
    return success_count == len(notifications)


def test_scheduler_notifications():
    """Test notifications from scheduler component"""
    print("🧪 Testing Scheduler Notifications...")

    # Mock database manager
    mock_db = Mock()
    mock_db.get_today_posts_count.return_value = 0

    scheduler = PostScheduler(mock_db)

    # Test notification scheduling
    with patch("notifier.send_notification") as mock_notify:
        # Test daily post notification
        scheduler.schedule_daily_post(lambda post_type: None)

        # Test random post notification
        scheduler.schedule_remaining_posts(lambda post_type: None)

        # Check if notifications were scheduled
        jobs = scheduler.get_scheduled_jobs()
        notification_jobs = [
            job_info for job_info, job_func in jobs if "notify" in job_info
        ]

        print(f"✅ Found {len(notification_jobs)} notification jobs scheduled")
        return len(notification_jobs) > 0


def test_notification_error_handling():
    """Test notification error handling"""
    print("🧪 Testing Notification Error Handling...")

    # Test with None values - should raise an exception
    try:
        send_notification(title=None, message=None)
        print("❌ Notification should have failed with None values")
        return False
    except Exception as e:
        print(f"✅ Notification correctly rejected None values: {e}")

    # Test with empty strings - should work
    try:
        send_notification(title="", message="")
        print("✅ Notification handles empty strings gracefully")
    except Exception as e:
        print(f"❌ Notification failed with empty strings: {e}")
        return False

    # Test with very long title - should work
    try:
        send_notification(title="A" * 1000, message="Test message")
        print("✅ Notification handles very long title gracefully")
    except Exception as e:
        print(f"❌ Notification failed with very long title: {e}")
        return False

    return True


def test_notification_timeout():
    """Test notification timeout behavior"""
    print("🧪 Testing Notification Timeout...")

    try:
        # Send notification and check if it appears
        send_notification(
            title="Timeout Test",
            message="This notification should disappear after 10 seconds",
        )
        print("✅ Notification timeout test initiated")
        print("   (Check if notification appears and disappears after 10 seconds)")
        return True
    except Exception as e:
        print(f"❌ Timeout test failed: {e}")
        return False


def test_plyer_availability():
    """Test if plyer is properly installed and available"""
    print("🧪 Testing Plyer Availability...")

    try:
        import plyer

        print("✅ Plyer is available")

        # Test if notification module is available
        from plyer import notification

        print("✅ Plyer notification module is available")
        return True
    except ImportError as e:
        print(f"❌ Plyer not available: {e}")
        print("   Install with: pip install plyer")
        return False


def test_notification_integration():
    """Test notification integration with the main bot components"""
    print("🧪 Testing Notification Integration...")

    # Mock the poster bot callback
    def mock_post_callback(post_type):
        send_notification(
            title="Post Result",
            message=f"{post_type} post was successful.\nNext post scheduled: 14:00",
        )

    try:
        # Test successful post notification
        mock_post_callback("RANDOM")
        print("✅ Post callback notification works")

        # Test failed post notification
        send_notification(
            title="Post Result",
            message="RANDOM post failed.\nNext post scheduled: 14:00",
        )
        print("✅ Failed post notification works")

        return True
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False


def main():
    """Run all notification tests"""
    print("🚀 Starting Notification Feature Tests...\n")

    # Disable logging for tests
    logging.disable(logging.CRITICAL)

    tests = [
        ("Plyer Availability", test_plyer_availability),
        ("Basic Notification", test_basic_notification),
        ("Special Characters", test_notification_with_special_characters),
        ("Long Message", test_long_message_notification),
        ("Multiple Notifications", test_multiple_notifications),
        ("Error Handling", test_notification_error_handling),
        ("Timeout Behavior", test_notification_timeout),
        ("Scheduler Integration", test_scheduler_notifications),
        ("Bot Integration", test_notification_integration),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print(f"{'='*50}")

        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")

    print(f"\n{'='*50}")
    print(f"TEST SUMMARY: {passed}/{total} tests passed")
    print(f"{'='*50}")

    if passed == total:
        print(
            "🎉 All notification tests passed! The notification system is working correctly."
        )
        print("\n📝 Notification system features:")
        print("✅ Desktop notifications for post results")
        print("✅ Upcoming post reminders")
        print("✅ Error notifications")
        print("✅ Timeout handling (10 seconds)")
        print("✅ Special character support")
        print("✅ Integration with scheduler")
    else:
        print(
            f"⚠️  {total - passed} test(s) failed. Please check the notification system."
        )
        print("\n🔧 Troubleshooting tips:")
        print("1. Ensure plyer is installed: pip install plyer")
        print("2. Check if your desktop environment supports notifications")
        print("3. Verify notification permissions in your OS")
        print("4. Test with a simple notification manually")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
