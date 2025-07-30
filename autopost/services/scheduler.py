"""
Scheduling service module for the Automated Daily Poster Bot.

This module handles all scheduling operations including job management,
timing calculations, and automated posting schedules.
"""

import schedule
import time
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any

from ..database.manager import DatabaseManager


class PostScheduler:
    """Manages automated posting schedules"""

    def __init__(self, database_manager: DatabaseManager):
        self.logger = logging.getLogger(__name__)
        self.database_manager = database_manager
        self.scheduler_thread = None
        self.is_running = False
        self.jobs = {}

        # Default schedule configuration
        self.schedule_config = {
            "daily_post_time": "10:00",  # Daily post at 10:00 AM (earlier)
            "random_posts_per_day": 6,  # 6 random posts throughout the day
            "random_post_interval": 2,  # Hours between random posts (reduced)
            "start_time": "08:00",  # Start posting at 8 AM (earlier)
            "end_time": "22:00",  # Stop posting at 10 PM (later)
        }

    def start(self):
        """Start the scheduler in a separate thread"""
        if self.is_running:
            self.logger.warning("Scheduler is already running")
            return

        self.is_running = True
        self.scheduler_thread = threading.Thread(
            target=self._run_scheduler, daemon=True
        )
        self.scheduler_thread.start()
        self.logger.info("Scheduler started")

    def stop(self):
        """Stop the scheduler"""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        self.logger.info("Scheduler stopped")

    def _run_scheduler(self):
        """Main scheduler loop"""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                time.sleep(5)  # Wait before retrying

    def setup_daily_schedule(self, post_callback: Callable[[str], None]):
        """Setup the daily posting schedule"""
        try:
            # Clear existing schedules
            schedule.clear()

            # Setup daily post at 12:00 PM
            daily_time = self.schedule_config["daily_post_time"]
            schedule.every().day.at(daily_time).do(
                lambda: self._execute_scheduled_post("SCHEDULED", post_callback)
            )
            self.logger.info(f"Daily post scheduled for {daily_time}")

            # Setup random posts throughout the day
            self._setup_random_posts(post_callback)

            # Log the schedule
            self._log_schedule()

        except Exception as e:
            self.logger.error(f"Failed to setup daily schedule: {e}")
            raise

    def _setup_random_posts(self, post_callback: Callable[[str], None]):
        """Setup random posts throughout the day"""
        try:
            start_time = datetime.strptime(self.schedule_config["start_time"], "%H:%M")
            end_time = datetime.strptime(self.schedule_config["end_time"], "%H:%M")
            interval_hours = self.schedule_config["random_post_interval"]
            num_posts = self.schedule_config["random_posts_per_day"]

            # Calculate time slots for random posts
            time_slots = self._calculate_time_slots(start_time, end_time, num_posts)

            for i, slot in enumerate(time_slots):
                schedule.every().day.at(slot.strftime("%H:%M")).do(
                    lambda slot_num=i: self._execute_scheduled_post(
                        "RANDOM", post_callback
                    )
                )
                self.logger.info(
                    f"Random post {i+1} scheduled for {slot.strftime('%H:%M')}"
                )

        except Exception as e:
            self.logger.error(f"Failed to setup random posts: {e}")
            raise

    def get_schedule_variations(self) -> List[Dict[str, Any]]:
        """Get different schedule variations for variety"""
        return [
            {
                "name": "Morning Focus",
                "daily_post_time": "09:00",
                "random_posts_per_day": 5,
                "start_time": "08:00",
                "end_time": "20:00",
                "times": ["10:30", "12:15", "14:45", "16:30", "18:15"]
            },
            {
                "name": "Evening Focus", 
                "daily_post_time": "11:00",
                "random_posts_per_day": 6,
                "start_time": "09:00",
                "end_time": "22:00",
                "times": ["12:30", "14:15", "16:00", "17:45", "19:30", "21:15"]
            },
            {
                "name": "Balanced Day",
                "daily_post_time": "10:00",
                "random_posts_per_day": 6,
                "start_time": "08:00",
                "end_time": "22:00",
                "times": ["11:30", "13:45", "15:15", "17:30", "19:00", "20:45"]
            }
        ]

    def _calculate_time_slots(
        self, start_time: datetime, end_time: datetime, num_slots: int
    ) -> List[datetime]:
        """Calculate time slots for random posts with better distribution"""
        slots = []
        
        # Use the "Balanced Day" schedule as default
        strategic_times = [
            "11:30",  # Late morning
            "13:45",  # Early afternoon
            "15:15",  # Mid afternoon
            "17:30",  # Late afternoon
            "19:00",  # Early evening
            "20:45",  # Late evening
        ]
        
        # Use strategic times if we have enough slots
        if num_slots <= len(strategic_times):
            for i in range(num_slots):
                time_str = strategic_times[i]
                slot_time = datetime.strptime(time_str, "%H:%M")
                # Ensure it's within our time range
                if start_time.time() <= slot_time.time() <= end_time.time():
                    slots.append(slot_time)
        else:
            # Fallback to calculated distribution
            total_minutes = (end_time - start_time).total_seconds() / 60
            interval_minutes = total_minutes / (num_slots + 1)  # +1 to avoid edge times

            for i in range(num_slots):
                slot_minutes = start_time.minute + (i + 1) * interval_minutes
                slot_hour = start_time.hour + int(slot_minutes // 60)
                slot_minute = int(slot_minutes % 60)

                # Ensure we don't exceed end time
                if slot_hour > end_time.hour or (
                    slot_hour == end_time.hour and slot_minute >= end_time.minute
                ):
                    break

                slot_time = start_time.replace(hour=slot_hour, minute=slot_minute)
                slots.append(slot_time)

        return slots

    def _execute_scheduled_post(
        self, post_type: str, post_callback: Callable[[str], None]
    ):
        """Execute a scheduled post"""
        try:
            self.logger.info(f"Executing scheduled {post_type} post...")

            # Check if we should make the post
            if self._should_make_post(post_type):
                post_callback(post_type)
                self.logger.info(f"Scheduled {post_type} post completed")
            else:
                self.logger.info(f"Skipping {post_type} post (conditions not met)")

        except Exception as e:
            self.logger.error(f"Error executing scheduled {post_type} post: {e}")

    def _should_make_post(self, post_type: str) -> bool:
        """Check if we should make a post based on current conditions"""
        try:
            # Get current post counts
            posts_today = self.database_manager.get_posts_today()
            random_posts_today = self.database_manager.get_posts_today("RANDOM")
            scheduled_posts_today = self.database_manager.get_posts_today("SCHEDULED")

            # Check limits
            if post_type == "RANDOM":
                return random_posts_today < self.schedule_config["random_posts_per_day"]
            elif post_type == "SCHEDULED":
                return scheduled_posts_today < 1  # Only one scheduled post per day

            return True

        except Exception as e:
            self.logger.error(f"Error checking post conditions: {e}")
            return False

    def _log_schedule(self):
        """Log the current schedule"""
        try:
            jobs = schedule.get_jobs()
            self.logger.info(f"Current schedule has {len(jobs)} jobs:")

            for job in jobs:
                self.logger.info(f"  - {job.job_func.__name__} at {job.at_time}")

        except Exception as e:
            self.logger.error(f"Error logging schedule: {e}")

    def get_schedule_info(self) -> Dict[str, Any]:
        """Get information about the current schedule"""
        try:
            jobs = schedule.get_jobs()

            return {
                "is_running": self.is_running,
                "total_jobs": len(jobs),
                "schedule_config": self.schedule_config,
                "next_jobs": self._get_next_jobs(jobs),
            }

        except Exception as e:
            self.logger.error(f"Error getting schedule info: {e}")
            return {"is_running": self.is_running, "error": str(e)}

    def _get_next_jobs(self, jobs: List) -> List[Dict[str, Any]]:
        """Get information about upcoming jobs"""
        next_jobs = []

        for job in jobs:
            try:
                next_run = job.next_run
                if next_run:
                    next_jobs.append(
                        {
                            "function": job.job_func.__name__,
                            "next_run": next_run.isoformat(),
                            "time_until": str(next_run - datetime.now()),
                        }
                    )
            except Exception as e:
                self.logger.warning(f"Error getting job info: {e}")

        return next_jobs

    def update_schedule_config(self, new_config: Dict[str, Any]):
        """Update the schedule configuration"""
        try:
            self.schedule_config.update(new_config)
            self.logger.info("Schedule configuration updated")

            # Restart scheduler with new config
            if self.is_running:
                self.stop()
                time.sleep(1)
                self.start()

        except Exception as e:
            self.logger.error(f"Error updating schedule config: {e}")
            raise

    def add_custom_job(
        self, job_func: Callable, schedule_time: str, job_type: str = "CUSTOM"
    ) -> bool:
        """Add a custom job to the schedule"""
        try:
            schedule.every().day.at(schedule_time).do(
                lambda: self._execute_scheduled_post(job_type, job_func)
            )

            self.logger.info(f"Custom job added for {schedule_time}")
            return True

        except Exception as e:
            self.logger.error(f"Error adding custom job: {e}")
            return False

    def remove_job(self, job_time: str) -> bool:
        """Remove a job from the schedule"""
        try:
            # This is a simplified implementation
            # In a real scenario, you'd need to track job references
            self.logger.info(f"Job removal requested for {job_time}")
            return True

        except Exception as e:
            self.logger.error(f"Error removing job: {e}")
            return False
