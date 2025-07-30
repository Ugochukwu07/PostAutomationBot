#!/usr/bin/env python3
"""
Automated Daily Poster Bot
Main entry point for the bot application
"""

import sys
import argparse
from .core.bot import AutomatedPosterBot


def main():
    """Main entry point for the Automated Poster Bot"""
    parser = argparse.ArgumentParser(description="Automated Daily Poster Bot")
    parser.add_argument("--test", action="store_true", help="Make a test post and exit")
    parser.add_argument(
        "--post", action="store_true", help="Make a real post on the spot and exit"
    )
    parser.add_argument(
        "--status", action="store_true", help="Show bot status and exit"
    )
    parser.add_argument("--daemon", action="store_true", help="Run in daemon mode")

    args = parser.parse_args()

    # Create bot instance
    bot = AutomatedPosterBot()

    try:
        if args.test:
            print("Making test post...")
            if bot.initialize():
                success = bot.make_test_post()
                if success:
                    print("✅ Test post successful!")
                else:
                    print("❌ Test post failed!")
                    sys.exit(1)
            else:
                print("❌ Bot initialization failed!")
                sys.exit(1)

        elif args.post:
            print("Making real post on the spot...")
            if bot.initialize():
                success = bot.make_post("RANDOM")
                if success:
                    print("✅ Post successful!")
                else:
                    print("❌ Post failed!")
                    sys.exit(1)
            else:
                print("❌ Bot initialization failed!")
                sys.exit(1)

        elif args.status:
            if bot.initialize():
                status = bot.get_status()
                print("\n🤖 Bot Status:")
                print(f"  Running: {'Yes' if status['is_running'] else 'No'}")
                print(f"  Posts Today: {status['posts_today']}")
                print(f"  Random Posts: {status['random_posts_today']}")
                print(f"  Scheduled Posts: {status['scheduled_posts_today']}")
                print(f"  Last Post: {status['last_post_time']}")
                print(f"  Scheduled Jobs: {status['scheduled_jobs']}")
            else:
                print("❌ Bot initialization failed!")
                sys.exit(1)

        else:
            print("🚀 Starting Automated Daily Poster Bot...")
            print("📋 Features:")
            print("  • Daily scheduled post at 12:00 PM")
            print("  • 5 random posts throughout the day")
            print("  • Multiple content sources from random APIs")
            print("  • API key authentication (RecentHPost)")
            print("  • MySQL logging")
            print("  • Intelligent scheduling")
            print("\nPress Ctrl+C to stop the bot\n")

            bot.start()

    except KeyboardInterrupt:
        print("\n🛑 Stopping bot...")
        bot.stop()
        print("👋 Bot stopped. Goodbye!")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        bot.stop()
        sys.exit(1)


if __name__ == "__main__":
    main()
