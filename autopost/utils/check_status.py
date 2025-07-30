#!/usr/bin/env python3
"""
Simple status checker that bypasses API connection requirement
"""

import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseManager


def main():
    """Check bot status from database"""
    print("🤖 Bot Status Check\n")

    db_manager = DatabaseManager()

    if db_manager.connect():
        print("✅ Database connection successful")

        # Get today's post count
        total_posts = db_manager.get_today_posts_count()
        random_posts = db_manager.get_today_posts_count("RANDOM")
        test_posts = db_manager.get_today_posts_count("TEST")
        scheduled_posts = db_manager.get_today_posts_count("SCHEDULED")

        print(f"📊 Today's Posts:")
        print(f"   Total: {total_posts}")
        print(f"   Random: {random_posts}")
        print(f"   Test: {test_posts}")
        print(f"   Scheduled: {scheduled_posts}")

        # Get last post time
        last_post = db_manager.get_last_post_time()
        if last_post:
            print(f"🕐 Last Post: {last_post}")
        else:
            print("🕐 Last Post: None")

        # Get recent posts
        print(f"\n📝 Recent Posts:")
        try:
            cursor = db_manager.connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT post_type, status, api_used, created_at, 
                       LEFT(content, 50) as content_preview
                FROM posts 
                ORDER BY created_at DESC 
                LIMIT 5
            """
            )

            posts = cursor.fetchall()
            if posts:
                for post in posts:
                    status_emoji = "✅" if post["status"] == "SUCCESS" else "❌"
                    print(f"   {status_emoji} {post['post_type']} - {post['api_used']}")
                    print(f"      {post['content_preview']}...")
                    print(f"      {post['created_at']}")
                    print()
            else:
                print("   No posts found")

            cursor.close()
        except Exception as e:
            print(f"   Error fetching posts: {e}")

    else:
        print("❌ Database connection failed")


if __name__ == "__main__":
    main()
