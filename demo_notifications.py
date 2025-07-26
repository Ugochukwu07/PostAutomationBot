#!/usr/bin/env python3
"""
Demo script for Notification Feature
Shows how notifications work in the Automated Daily Poster Bot
"""

import os
import sys
import time

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from notifier import send_notification

def demo_basic_notifications():
    """Demonstrate basic notification functionality"""
    print("🚀 Notification Feature Demo")
    print("=" * 50)
    
    print("\n1. Basic notification...")
    send_notification(
        title="Bot Status",
        message="Automated Poster Bot is running successfully!"
    )
    time.sleep(2)
    
    print("\n2. Post result notification...")
    send_notification(
        title="Post Result",
        message="RANDOM post was successful.\nNext post scheduled: 14:00"
    )
    time.sleep(2)
    
    print("\n3. Upcoming post reminder...")
    send_notification(
        title="Upcoming Post",
        message="A SCHEDULED post is at 12:00"
    )
    time.sleep(2)
    
    print("\n4. Error notification...")
    send_notification(
        title="Post Error",
        message="Failed to post content. Retrying in 5 minutes..."
    )
    time.sleep(2)
    
    print("\n5. Special characters and emojis...")
    send_notification(
        title="🎉 Bot Update",
        message="✅ Post successful!\n📝 Content: Random quote\n⏰ Time: 10:30 AM"
    )
    time.sleep(2)
    
    print("\n6. Long message test...")
    send_notification(
        title="Detailed Report",
        message="Today's posting summary:\n• 3 random posts completed\n• 1 scheduled post completed\n• 0 failed posts\n• Next post in 2 hours"
    )
    
    print("\n✅ All demo notifications sent!")
    print("\n📝 Notification Features Demonstrated:")
    print("• Basic desktop notifications")
    print("• Post result notifications")
    print("• Upcoming post reminders")
    print("• Error notifications")
    print("• Emoji and special character support")
    print("• Multi-line messages")
    print("• 10-second timeout")

if __name__ == "__main__":
    demo_basic_notifications() 