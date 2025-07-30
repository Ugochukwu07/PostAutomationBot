"""
Core bot module for the Automated Daily Poster Bot.

This module contains the main bot class that orchestrates all automated
posting operations and manages the overall bot lifecycle.
"""

import logging
import time
import threading
import random
from datetime import datetime
from typing import Dict, Optional, List

from ..config.settings import Config
from ..database.manager import DatabaseManager
from ..content.fetcher import ContentFetcher
from ..api.client import APIClient
from ..services.scheduler import PostScheduler
from ..utils.notifier import (
    send_notification,
    send_post_notification,
    send_error_notification,
)


class AutomatedPosterBot:
    """Main bot class that orchestrates automated posting"""

    def __init__(self):
        self.logger = self._setup_logging()
        self.logger.info("Initializing Automated Poster Bot...")

        # Initialize components
        self.database_manager = DatabaseManager()
        self.content_fetcher = ContentFetcher()
        self.api_client = APIClient()
        self.scheduler = PostScheduler(self.database_manager)

        # Bot state
        self.is_running = False
        self.scheduler_thread = None

        self.logger.info("Bot initialization complete")

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        log_file_path = Config.get_log_file_path()

        logging.basicConfig(
            level=getattr(logging, Config.Bot.LOG_LEVEL),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()],
        )

        return logging.getLogger(__name__)

    def initialize(self) -> bool:
        """Initialize the bot and test all connections"""
        try:
            self.logger.info("Starting bot initialization...")

            # Validate configuration
            if not Config.validate_config():
                self.logger.error("Configuration validation failed")
                return False

            self.logger.info("Configuration validated")

            # Test database connection
            if not self.database_manager.connect():
                self.logger.error("Failed to connect to database")
                return False

            # Create database tables
            self.database_manager.create_tables()
            self.logger.info("Database tables verified")

            # Test API connection
            api_connected = self.api_client.test_connection()
            if not api_connected:
                self.logger.warning("Failed to test API connection - bot will run in limited mode")
                self.logger.warning("Posts will be logged but not sent to external API")
                # Don't return False here - allow bot to start with limited functionality
            else:
                self.logger.info("API connection test successful")

            self.logger.info("Bot initialization completed")
            return True

        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            send_error_notification(str(e), "Bot Initialization")
            return False

    def make_post(self, post_type: str = "RANDOM") -> bool:
        """Make a single post with content from random API"""
        try:
            self.logger.info(f"Making {post_type} post...")

            # Fetch content from random API
            try:
                content_data = self.content_fetcher.fetch_content()
                content = content_data["content"]
                api_name = content_data["api_name"]
                title = content_data.get("title")
                self.logger.info(f"Content fetched from: {api_name}")
            except Exception as e:
                self.logger.warning(f"Failed to fetch content from APIs: {e}")
                content_data = self.content_fetcher.get_fallback_content()
                content = content_data["content"]
                api_name = content_data["api_name"]
                title = content_data.get("title")
                self.logger.info("Using fallback content")

            # Generate hashtags
            hashtags = self._generate_smart_hashtags(content, api_name)

            # Post to API
            result = self.api_client.post_content(
                content=content, title=title, hashtags=hashtags
            )

            # Log the post attempt
            post_id = self.database_manager.log_post(
                post_type=post_type,
                content=content,
                title=title,
                hashtags=hashtags,
                api_source=api_name,
                status="success" if result["success"] else "failed",
                error_message=result.get("error"),
            )

            # Update bot status
            if result["success"]:
                self._update_post_counters(post_type)
                self.logger.info(f"Post successful (ID: {post_id})")

                # Send notification
                send_post_notification(post_type, True, content[:100])

                return True
            else:
                self.logger.error(f"Post failed: {result.get('error')}")
                send_post_notification(post_type, False, content[:100])
                return False

        except Exception as e:
            self.logger.error(f"Error making post: {e}")
            send_error_notification(str(e), f"{post_type} Post Error")
            return False

    def _generate_smart_hashtags(self, content: str, api_name: str) -> List[str]:
        """Generate relevant hashtags based on content and API source"""
        hashtags = []

        # Add API-specific hashtags
        api_hashtags = {
            "Quotes API": ["#quote", "#inspiration", "#motivation"],
            "Joke API": ["#joke", "#humor", "#funny"],
            "Advice API": ["#advice", "#wisdom", "#tips"],
            "Useless Facts API": ["#facts", "#trivia", "#knowledge"],
            "Dog Facts API": ["#dogs", "#pets", "#animals"],
            "Random Word API": ["#word", "#vocabulary", "#language"],
            "Bored API": ["#activity", "#ideas", "#fun"],
            "Fallback Content": ["#motivation", "#inspiration", "#life"],
        }

        hashtags.extend(api_hashtags.get(api_name, ["#autopost", "#bot"]))

        # Add content-based hashtags
        content_lower = content.lower()

        if any(word in content_lower for word in ["success", "achieve", "goal"]):
            hashtags.extend(["#success", "#goals"])
        if any(word in content_lower for word in ["love", "heart", "relationship"]):
            hashtags.extend(["#love", "#relationships"])
        if any(word in content_lower for word in ["work", "career", "job"]):
            hashtags.extend(["#work", "#career"])
        if any(word in content_lower for word in ["health", "fitness", "exercise"]):
            hashtags.extend(["#health", "#fitness"])

        # Ensure we don't have too many hashtags
        hashtags = list(set(hashtags))[:5]  # Max 5 hashtags

        return hashtags

    def _update_post_counters(self, post_type: str):
        """Update post counters in database"""
        try:
            # Get current counts
            posts_today = self.database_manager.get_posts_today()
            random_posts_today = self.database_manager.get_posts_today("RANDOM")
            scheduled_posts_today = self.database_manager.get_posts_today("SCHEDULED")

            # Update based on post type
            if post_type == "RANDOM":
                random_posts_today += 1
            elif post_type == "SCHEDULED":
                scheduled_posts_today += 1

            posts_today += 1

            # Update database
            self.database_manager.update_bot_status(
                posts_today=posts_today,
                random_posts_today=random_posts_today,
                scheduled_posts_today=scheduled_posts_today,
                last_post_time=datetime.now(),
            )

        except Exception as e:
            self.logger.error(f"Error updating post counters: {e}")

    def post_callback(self, post_type: str):
        """Callback function for scheduled posts"""
        try:
            self.logger.info(f"Scheduled {post_type} post triggered")

            # Check if we should make the post
            if post_type == "RANDOM":
                posts_today = self.database_manager.get_posts_today("RANDOM")
                if posts_today >= 5:  # Max 5 random posts per day
                    self.logger.info("Random post limit reached for today")
                    return
            elif post_type == "SCHEDULED":
                posts_today = self.database_manager.get_posts_today("SCHEDULED")
                if posts_today >= 1:  # Max 1 scheduled post per day
                    self.logger.info("Scheduled post already made today")
                    return

            # Make the post
            success = self.make_post(post_type)

            if success:
                self.logger.info(f"Scheduled {post_type} post completed successfully")
            else:
                self.logger.error(f"Scheduled {post_type} post failed")

        except Exception as e:
            self.logger.error(f"Error in post callback: {e}")
            send_error_notification(str(e), f"Scheduled {post_type} Post Error")

    def start(self):
        """Start the bot and begin automated posting"""
        try:
            if not self.initialize():
                raise Exception("Bot initialization failed")

            self.logger.info("Starting Automated Poster Bot...")

            # Update bot status
            self.database_manager.update_bot_status(is_running=True)

            # Setup and start scheduler
            self.scheduler.setup_daily_schedule(self.post_callback)
            self.scheduler.start()

            self.is_running = True

            self.logger.info("Bot started successfully")

            # Keep the main thread alive
            try:
                while self.is_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("Received interrupt signal")
                self.stop()

        except Exception as e:
            self.logger.error(f"Error starting bot: {e}")
            send_error_notification(str(e), "Bot Start Error")
            self.stop()
            raise

    def stop(self):
        """Stop the bot and cleanup resources"""
        try:
            self.logger.info("Stopping Automated Poster Bot...")

            # Stop scheduler
            if self.scheduler:
                self.scheduler.stop()

            # Update bot status
            self.database_manager.update_bot_status(is_running=False)

            # Close database connection
            self.database_manager.disconnect()

            self.is_running = False

            self.logger.info("Bot stopped successfully")

        except Exception as e:
            self.logger.error(f"Error stopping bot: {e}")

    def get_status(self) -> Dict:
        """Get current bot status"""
        try:
            # Get database status
            db_status = self.database_manager.get_bot_status()

            # Get scheduler info
            scheduler_info = self.scheduler.get_schedule_info()

            # Combine status information
            status = {
                "is_running": self.is_running and db_status.get("is_running", False),
                "posts_today": db_status.get("posts_today", 0),
                "random_posts_today": db_status.get("random_posts_today", 0),
                "scheduled_posts_today": db_status.get("scheduled_posts_today", 0),
                "last_post_time": db_status.get("last_post_time"),
                "scheduled_jobs": scheduler_info.get("total_jobs", 0),
                "scheduler_running": scheduler_info.get("is_running", False),
                "next_jobs": scheduler_info.get("next_jobs", []),
            }

            return status

        except Exception as e:
            self.logger.error(f"Error getting status: {e}")
            return {"is_running": False, "error": str(e)}

    def make_test_post(self) -> bool:
        """Make a test post to verify functionality"""
        try:
            self.logger.info("Making test post...")

            # Use a simple test content
            test_content = (
                "This is a test post from the Automated Poster Bot. 🤖 #test #autopost"
            )

            # Check if API is available
            if not self.api_client.test_connection():
                self.logger.warning("API not available - logging test post to database only")
                
                # Log the test post to database
                post_id = self.database_manager.log_post(
                    post_type="TEST",
                    content=test_content,
                    title="Test Post",
                    hashtags=["#test", "#autopost", "#bot"],
                    api_source="Test Mode",
                    status="success",
                    error_message="API not available - logged to database only",
                )
                
                # Update bot status counters
                self._update_post_counters("TEST")
                
                self.logger.info(f"Test post logged to database (ID: {post_id})")
                return True

            result = self.api_client.post_content(
                content=test_content,
                title="Test Post",
                hashtags=["#test", "#autopost", "#bot"],
            )

            if result["success"]:
                # Update bot status counters
                self._update_post_counters("TEST")
                self.logger.info("Test post successful")
                return True
            else:
                self.logger.error(f"Test post failed: {result.get('error')}")
                return False

        except Exception as e:
            self.logger.error(f"Error making test post: {e}")
            return False
