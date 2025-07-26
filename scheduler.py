import schedule
import time
import random
import logging
from datetime import datetime, timedelta
from typing import List, Tuple
from database import DatabaseManager
from notifier import send_notification

class PostScheduler:
    """Handles intelligent scheduling of posts throughout the day"""
    
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager
        self.logger = logging.getLogger(__name__)
        
        # Constants
        self.SCHEDULED_POST_TIME = "12:00"  # 12 PM daily
        self.RANDOM_POSTS_PER_DAY = 5
        self.MIN_INTERVAL_MINUTES = 30  # Minimum time between posts
        self.MAX_INTERVAL_MINUTES = 240  # Maximum time between posts (4 hours)
    
    def calculate_remaining_posts(self) -> int:
        """Calculate how many random posts are still needed today"""
        total_posts_today = self.database_manager.get_today_posts_count()
        random_posts_today = self.database_manager.get_today_posts_count('RANDOM')
        
        # We need 5 random posts per day
        remaining_random_posts = max(0, self.RANDOM_POSTS_PER_DAY - random_posts_today)
        
        self.logger.info(f"Posts today: {total_posts_today}, Random posts: {random_posts_today}, Remaining: {remaining_random_posts}")
        
        return remaining_random_posts
    
    def calculate_time_remaining_today(self) -> float:
        """Calculate how many hours remain until midnight"""
        now = datetime.now()
        midnight = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        time_remaining = (midnight - now).total_seconds() / 3600  # Convert to hours
        
        return time_remaining
    
    def distribute_posts_intelligently(self, num_posts: int, hours_remaining: float) -> List[datetime]:
        """Intelligently distribute posts over the remaining time"""
        if num_posts <= 0 or hours_remaining <= 0:
            return []
        
        # Convert hours to minutes for easier calculation
        minutes_remaining = hours_remaining * 60
        
        # Calculate minimum and maximum intervals
        min_interval = max(self.MIN_INTERVAL_MINUTES, minutes_remaining / (num_posts + 1))
        max_interval = min(self.MAX_INTERVAL_MINUTES, minutes_remaining / num_posts)
        
        # Ensure max_interval is at least min_interval
        max_interval = max(max_interval, min_interval)
        
        self.logger.info(f"Distributing {num_posts} posts over {hours_remaining:.1f} hours")
        self.logger.info(f"Interval range: {min_interval:.1f} - {max_interval:.1f} minutes")
        
        post_times = []
        current_time = datetime.now()
        
        for i in range(num_posts):
            # Calculate interval for this post
            if i == 0:
                # First post: wait a bit to avoid immediate posting
                interval = random.uniform(min_interval, min_interval * 2)
            else:
                # Subsequent posts: random interval within range
                interval = random.uniform(min_interval, max_interval)
            
            # Calculate post time
            post_time = current_time + timedelta(minutes=interval)
            
            # Ensure we don't go past midnight
            if post_time.hour >= 23:
                post_time = post_time.replace(hour=22, minute=random.randint(0, 59))
            
            post_times.append(post_time)
            current_time = post_time
        
        return sorted(post_times)
    
    def schedule_remaining_posts(self, callback_function):
        """Schedule the remaining random posts for today"""
        remaining_posts = self.calculate_remaining_posts()
        
        if remaining_posts == 0:
            self.logger.info("No remaining random posts to schedule for today")
            return
        
        hours_remaining = self.calculate_time_remaining_today()
        
        if hours_remaining <= 0:
            self.logger.warning("No time remaining today to schedule posts")
            return
        
        post_times = self.distribute_posts_intelligently(remaining_posts, hours_remaining)
        
        for i, post_time in enumerate(post_times):
            self.logger.info(f"Scheduling random post {i+1}/{len(post_times)} at {post_time.strftime('%H:%M:%S')}")
            
            # Schedule the post
            schedule.every().day.at(post_time.strftime("%H:%M")).do(
                callback_function, post_type="RANDOM"
            ).tag(f"random_post_{i}")
            # Schedule notification 1 hour before
            notify_time = (post_time - timedelta(hours=1)).strftime("%H:%M")
            schedule.every().day.at(notify_time).do(
                send_notification,
                title="Upcoming Post",
                message=f"A RANDOM post is scheduled at {post_time.strftime('%H:%M')}"
            ).tag(f"notify_random_post_{i}")
    
    def schedule_daily_post(self, callback_function):
        """Schedule the daily 12 PM post"""
        self.logger.info(f"Scheduling daily post at {self.SCHEDULED_POST_TIME}")
        
        schedule.every().day.at(self.SCHEDULED_POST_TIME).do(
            callback_function, post_type="SCHEDULED"
        ).tag("daily_post")
        # Schedule notification 1 hour before daily post
        notify_time = (datetime.strptime(self.SCHEDULED_POST_TIME, "%H:%M") - timedelta(hours=1)).strftime("%H:%M")
        schedule.every().day.at(notify_time).do(
            send_notification,
            title="Upcoming Post",
            message=f"A SCHEDULED post is at {self.SCHEDULED_POST_TIME}"
        ).tag("notify_daily_post")
    
    def clear_all_schedules(self):
        """Clear all scheduled jobs"""
        schedule.clear()
        self.logger.info("All scheduled jobs cleared")
    
    def clear_random_posts(self):
        """Clear only random post schedules"""
        schedule.clear("random_post")
        self.logger.info("Random post schedules cleared")
    
    def get_scheduled_jobs(self) -> List[Tuple[str, str]]:
        """Get list of currently scheduled jobs"""
        jobs = []
        for job in schedule.jobs:
            job_info = f"{job.at_time} - {job.tags}"
            jobs.append((job_info, str(job.job_func)))
        
        return jobs
    
    def run_scheduler(self):
        """Run the scheduler loop"""
        self.logger.info("Starting scheduler loop...")
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                self.logger.info("Scheduler interrupted by user")
                break
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                time.sleep(60)  # Wait before retrying
    
    def initialize_daily_schedule(self, callback_function):
        """Initialize the complete daily schedule"""
        # Clear any existing schedules
        self.clear_all_schedules()
        
        # Schedule the daily 12 PM post
        self.schedule_daily_post(callback_function)
        
        # Schedule remaining random posts for today
        self.schedule_remaining_posts(callback_function)
        
        # Log current schedule
        jobs = self.get_scheduled_jobs()
        self.logger.info(f"Daily schedule initialized with {len(jobs)} jobs")
        for job_info, job_func in jobs:
            self.logger.info(f"  - {job_info}") 