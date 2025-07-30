"""
Database management module for the Automated Daily Poster Bot.

This module handles all database operations including connection management,
table creation, and post logging.
"""

import logging
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
import json

from ..config.settings import Config


class DatabaseManager:
    """Manages database connections and operations"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.connection = None
        self._connection_params = {
            "host": Config.Database.HOST,
            "port": Config.Database.PORT,
            "database": Config.Database.NAME,
            "user": Config.Database.USER,
            "password": Config.Database.PASSWORD,
            "charset": "utf8mb4",
            "collation": "utf8mb4_unicode_ci",
        }

    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**self._connection_params)
            self.logger.info("Database connection established successfully")
            return True
        except Error as e:
            self.logger.error(f"Failed to connect to database: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("Database connection closed")

    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                raise Exception("Failed to connect to database")

        cursor = self.connection.cursor(dictionary=True)
        try:
            yield cursor
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            cursor.close()

    def create_tables(self):
        """Create necessary database tables if they don't exist"""
        tables_sql = {
            "posts": """
                CREATE TABLE IF NOT EXISTS posts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    post_type VARCHAR(50) NOT NULL,
                    content TEXT NOT NULL,
                    title VARCHAR(255),
                    hashtags JSON,
                    api_source VARCHAR(100),
                    status VARCHAR(50) DEFAULT 'success',
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    posted_at TIMESTAMP NULL,
                    INDEX idx_post_type (post_type),
                    INDEX idx_created_at (created_at),
                    INDEX idx_status (status)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            "bot_status": """
                CREATE TABLE IF NOT EXISTS bot_status (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    is_running BOOLEAN DEFAULT FALSE,
                    last_post_time TIMESTAMP NULL,
                    posts_today INT DEFAULT 0,
                    random_posts_today INT DEFAULT 0,
                    scheduled_posts_today INT DEFAULT 0,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_is_running (is_running),
                    INDEX idx_updated_at (updated_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            "scheduled_jobs": """
                CREATE TABLE IF NOT EXISTS scheduled_jobs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    job_type VARCHAR(50) NOT NULL,
                    schedule_time TIME NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    last_run TIMESTAMP NULL,
                    next_run TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_job_type (job_type),
                    INDEX idx_is_active (is_active),
                    INDEX idx_next_run (next_run)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
        }

        try:
            with self.get_cursor() as cursor:
                for table_name, sql in tables_sql.items():
                    cursor.execute(sql)
                    self.logger.info(
                        f"Table '{table_name}' created/verified successfully"
                    )

            # Insert default bot status if not exists
            self._initialize_bot_status()

        except Exception as e:
            self.logger.error(f"Failed to create tables: {e}")
            raise

    def _initialize_bot_status(self):
        """Initialize bot status record if it doesn't exist"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as count FROM bot_status")
                if cursor.fetchone()["count"] == 0:
                    cursor.execute(
                        """
                        INSERT INTO bot_status (is_running, posts_today, random_posts_today, scheduled_posts_today)
                        VALUES (FALSE, 0, 0, 0)
                    """
                    )
                    self.logger.info("Bot status initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize bot status: {e}")

    def log_post(
        self,
        post_type: str,
        content: str,
        title: str = None,
        hashtags: List[str] = None,
        api_source: str = None,
        status: str = "success",
        error_message: str = None,
    ) -> int:
        """Log a post attempt to the database"""
        try:
            with self.get_cursor() as cursor:
                sql = """
                    INSERT INTO posts (post_type, content, title, hashtags, api_source, status, error_message, posted_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    post_type,
                    content,
                    title,
                    json.dumps(hashtags) if hashtags else None,
                    api_source,
                    status,
                    error_message,
                    datetime.now() if status == "success" else None,
                )

                cursor.execute(sql, values)
                post_id = cursor.lastrowid

                self.logger.info(f"Post logged with ID: {post_id}")
                return post_id

        except Exception as e:
            self.logger.error(f"Failed to log post: {e}")
            raise

    def update_bot_status(
        self,
        is_running: bool = None,
        last_post_time: datetime = None,
        posts_today: int = None,
        random_posts_today: int = None,
        scheduled_posts_today: int = None,
    ):
        """Update bot status in the database"""
        try:
            with self.get_cursor() as cursor:
                update_fields = []
                values = []

                if is_running is not None:
                    update_fields.append("is_running = %s")
                    values.append(is_running)

                if last_post_time is not None:
                    update_fields.append("last_post_time = %s")
                    values.append(last_post_time)

                if posts_today is not None:
                    update_fields.append("posts_today = %s")
                    values.append(posts_today)

                if random_posts_today is not None:
                    update_fields.append("random_posts_today = %s")
                    values.append(random_posts_today)

                if scheduled_posts_today is not None:
                    update_fields.append("scheduled_posts_today = %s")
                    values.append(scheduled_posts_today)

                if update_fields:
                    sql = (
                        f"UPDATE bot_status SET {', '.join(update_fields)} WHERE id = 1"
                    )
                    cursor.execute(sql, values)
                    self.logger.info("Bot status updated successfully")

        except Exception as e:
            self.logger.error(f"Failed to update bot status: {e}")
            raise

    def get_bot_status(self) -> Dict[str, Any]:
        """Get current bot status from database"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT * FROM bot_status WHERE id = 1")
                status = cursor.fetchone()

                if not status:
                    return {
                        "is_running": False,
                        "last_post_time": None,
                        "posts_today": 0,
                        "random_posts_today": 0,
                        "scheduled_posts_today": 0,
                    }

                return dict(status)

        except Exception as e:
            self.logger.error(f"Failed to get bot status: {e}")
            return {
                "is_running": False,
                "last_post_time": None,
                "posts_today": 0,
                "random_posts_today": 0,
                "scheduled_posts_today": 0,
            }

    def get_posts_today(self, post_type: str = None) -> int:
        """Get number of posts made today"""
        try:
            with self.get_cursor() as cursor:
                if post_type:
                    sql = """
                        SELECT COUNT(*) as count FROM posts 
                        WHERE DATE(created_at) = CURDATE() AND post_type = %s
                    """
                    cursor.execute(sql, (post_type,))
                else:
                    sql = "SELECT COUNT(*) as count FROM posts WHERE DATE(created_at) = CURDATE()"
                    cursor.execute(sql)

                result = cursor.fetchone()
                return result["count"] if result else 0

        except Exception as e:
            self.logger.error(f"Failed to get posts count: {e}")
            return 0

    def get_last_post_time(self) -> Optional[datetime]:
        """Get the timestamp of the last successful post"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT posted_at FROM posts 
                    WHERE status = 'success' AND posted_at IS NOT NULL
                    ORDER BY posted_at DESC LIMIT 1
                """
                )
                result = cursor.fetchone()
                return result["posted_at"] if result else None

        except Exception as e:
            self.logger.error(f"Failed to get last post time: {e}")
            return None
