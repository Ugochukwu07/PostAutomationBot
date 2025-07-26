import logging
import time
import threading
from datetime import datetime
from typing import Dict, Optional

from config import Config
from database import DatabaseManager
from content_fetcher import ContentFetcher
from api_client import APIClient
from scheduler import PostScheduler
from notifier import send_notification

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
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('autopost_bot.log'),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    def initialize(self) -> bool:
        """Initialize the bot and test all connections"""
        try:
            self.logger.info("Starting bot initialization...")
            
            # Validate configuration
            Config.validate_config()
            self.logger.info("Configuration validated")
            
            # Test database connection
            if not self.database_manager.connect():
                self.logger.error("Failed to connect to database")
                return False
            
            # Create database tables
            self.database_manager.create_tables()
            self.logger.info("Database tables verified")
            
            # Test API connection
            if not self.api_client.test_connection():
                self.logger.error("Failed to test API connection")
                return False
            
            self.logger.info("All connections tested successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            return False
    
    def make_post(self, post_type: str = "RANDOM") -> bool:
        """Make a single post with content from random API"""
        try:
            self.logger.info(f"Making {post_type} post...")
            
            # Fetch content from random API
            try:
                content_data = self.content_fetcher.fetch_content()
                content = content_data['content']
                api_name = content_data['api_name']
                title = content_data.get('title')  # Get title from API if available
                self.logger.info(f"Content fetched from: {api_name}")
            except Exception as e:
                self.logger.warning(f"Failed to fetch content from APIs: {e}")
                content_data = self.content_fetcher.get_fallback_content()
                content = content_data['content']
                api_name = content_data['api_name']
                title = content_data.get('title')  # Get title from fallback
                self.logger.info("Using fallback content")
            

            hashtags = self._generate_smart_hashtags(content, api_name)
            # Generate title and hashtags based on post type
            # if post_type == "RANDOM":
                # For random posts: use title from API if available, otherwise no title
                # Generate smart hashtags from content
                # hashtags = self._generate_smart_hashtags(content, api_name)
            # else:
            #     # For other posts: use title from API if available, otherwise use default
            #     if not title:
            #         title = f"{post_type} Post - {api_name}"
            #     hashtags = [f"#{post_type.lower()}", "#autopost", "#bot"]
            
            # Post content to API
            result = self.api_client.post_content(
                content=content,
                title=title,
                hashtags=hashtags
            )
            
            if result['success']:
                # Log successful post
                self.database_manager.log_post(
                    post_type=post_type,
                    status="SUCCESS",
                    api_used=api_name,
                    content=content[:500]  # Truncate for database storage
                )
                
                self.logger.info(f"{post_type} post successful")
                return True
            else:
                # Log failed post
                error_msg = result.get('error', 'Unknown error')
                self.database_manager.log_post(
                    post_type=post_type,
                    status="FAILURE",
                    api_used=api_name,
                    content=content[:500],
                    error_message=error_msg
                )
                
                self.logger.error(f"{post_type} post failed: {error_msg}")
                return False
                
        except Exception as e:
            self.logger.error(f"Unexpected error making {post_type} post: {e}")
            
            # Log the error
            self.database_manager.log_post(
                post_type=post_type,
                status="FAILURE",
                api_used="Unknown",
                error_message=str(e)
            )
            
            return False
    
    def _generate_smart_hashtags(self, content: str, api_name: str) -> list:
        """Generate smart hashtags from content without '#' prefix"""
        hashtags = []
        
        # Extract keywords from content based on API type
        if api_name == "Quotes API":
            # For quotes, extract inspirational words
            inspirational_words = ["inspiration", "motivation", "success", "life", "dreams", "goals", "wisdom", "quote"]
            hashtags = [word for word in inspirational_words if word.lower() in content.lower()]
        elif api_name == "Joke API":
            # For jokes, extract humor-related words
            humor_words = ["funny", "humor", "joke", "laugh", "comedy", "wit"]
            hashtags = [word for word in humor_words if word.lower() in content.lower()]
        elif api_name == "Advice API":
            # For advice, extract advice-related words
            advice_words = ["advice", "tips", "help", "guidance", "wisdom", "life"]
            hashtags = [word for word in advice_words if word.lower() in content.lower()]
        elif api_name == "Useless Facts API":
            # For facts, extract interesting words
            fact_words = ["fact", "interesting", "knowledge", "learn", "science", "amazing"]
            hashtags = [word for word in fact_words if word.lower() in content.lower()]
        elif api_name == "Dog Facts API":
            # For dog facts, extract animal-related words
            animal_words = ["dog", "pet", "animal", "puppy", "canine"]
            hashtags = [word for word in animal_words if word.lower() in content.lower()]
        elif api_name == "Random Word API":
            # For random words, extract word-related terms
            word_words = ["word", "vocabulary", "language", "learning"]
            hashtags = [word for word in word_words if word.lower() in content.lower()]
        elif api_name == "Bored API":
            # For bored activities, extract activity-related words
            activity_words = ["activity", "fun", "entertainment", "hobby", "leisure"]
            hashtags = [word for word in activity_words if word.lower() in content.lower()]
        else:
            # Generic content analysis
            common_words = ["life", "love", "success", "happiness", "motivation", "inspiration"]
            hashtags = [word for word in common_words if word.lower() in content.lower()]
        
        # If no hashtags found, use some generic ones based on content length
        if not hashtags:
            if len(content) < 100:
                hashtags = ["short", "quick"]
            elif len(content) > 200:
                hashtags = ["long", "detailed"]
            else:
                hashtags = ["content"]
        
        # Limit to 3 hashtags maximum
        return hashtags[:3]
    
    def post_callback(self, post_type: str):
        """Callback function for scheduled posts"""
        self.logger.info(f"Executing scheduled {post_type} post")
        
        success = self.make_post(post_type)
        
        # Notify result
        if success:
            result_msg = f"{post_type} post was successful."
        else:
            result_msg = f"{post_type} post failed."
        # Find next scheduled post
        jobs = self.scheduler.get_scheduled_jobs()
        next_job = None
        for job_info, job_func in jobs:
            if post_type.lower() in job_info.lower():
                continue  # skip current
            next_job = job_info
            break
        if next_job:
            next_msg = f"Next post scheduled: {next_job.split(' - ')[0]}"
        else:
            next_msg = "No more posts scheduled today."
        send_notification(
            title="Post Result",
            message=f"{result_msg}\n{next_msg}"
        )
        
        if success and post_type == "RANDOM":
            # If this was a random post, reschedule remaining posts
            self.scheduler.schedule_remaining_posts(self.post_callback)
    
    def start(self):
        """Start the automated poster bot"""
        if self.is_running:
            self.logger.warning("Bot is already running")
            return
        
        if not self.initialize():
            self.logger.error("Failed to initialize bot")
            return
        
        self.logger.info("Starting Automated Poster Bot...")
        self.is_running = True
        
        # Initialize daily schedule
        self.scheduler.initialize_daily_schedule(self.post_callback)
        
        # Start scheduler in a separate thread
        self.scheduler_thread = threading.Thread(target=self.scheduler.run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        self.logger.info("Bot started successfully")
        
        try:
            # Keep main thread alive
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal")
            self.stop()
    
    def stop(self):
        """Stop the automated poster bot"""
        if not self.is_running:
            return
        
        self.logger.info("Stopping Automated Poster Bot...")
        self.is_running = False
        
        # Clear all schedules
        self.scheduler.clear_all_schedules()
        
        # Close database connection
        self.database_manager.disconnect()
        
        self.logger.info("Bot stopped successfully")
    
    def get_status(self) -> Dict:
        """Get current bot status"""
        return {
            'is_running': self.is_running,
            'posts_today': self.database_manager.get_today_posts_count(),
            'random_posts_today': self.database_manager.get_today_posts_count('RANDOM'),
            'scheduled_posts_today': self.database_manager.get_today_posts_count('SCHEDULED'),
            'last_post_time': self.database_manager.get_last_post_time(),
            'scheduled_jobs': len(self.scheduler.get_scheduled_jobs())
        }
    
    def make_test_post(self) -> bool:
        """Make a test post to verify everything is working"""
        self.logger.info("Making test post...")
        return self.make_post("TEST") 