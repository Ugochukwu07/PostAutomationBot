import mysql.connector
from mysql.connector import Error
import logging
from datetime import datetime
from config import Config

class DatabaseManager:
    """Manages database connections and operations for the poster bot"""
    
    def __init__(self):
        self.connection = None
        self.logger = logging.getLogger(__name__)
    
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                autocommit=True
            )
            
            if self.connection.is_connected():
                self.logger.info("Successfully connected to MySQL database")
                return True
                
        except Error as e:
            self.logger.error(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("Database connection closed")
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            cursor = self.connection.cursor()
            
            # Create posts table
            create_posts_table = """
            CREATE TABLE IF NOT EXISTS posts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                post_type ENUM('SCHEDULED', 'RANDOM', 'TEST') NOT NULL,
                timestamp DATETIME NOT NULL,
                status ENUM('SUCCESS', 'FAILURE') NOT NULL,
                api_used VARCHAR(255),
                content TEXT,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(create_posts_table)
            self.logger.info("Posts table created/verified successfully")
            
        except Error as e:
            self.logger.error(f"Error creating tables: {e}")
            raise
    
    def log_post(self, post_type, status, api_used=None, content=None, error_message=None):
        """Log a post attempt to the database"""
        try:
            cursor = self.connection.cursor()
            
            insert_query = """
            INSERT INTO posts (post_type, timestamp, status, api_used, content, error_message)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                post_type,
                datetime.now(),
                status,
                api_used,
                content,
                error_message
            ))
            
            # Commit the transaction
            self.connection.commit()
            
            self.logger.info(f"Post logged: {post_type} - {status}")
            
        except Error as e:
            self.logger.error(f"Error logging post: {e}")
    
    def get_today_posts_count(self, post_type=None):
        """Get count of posts made today"""
        try:
            cursor = self.connection.cursor()
            
            if post_type:
                query = """
                SELECT COUNT(*) FROM posts 
                WHERE DATE(timestamp) = CURDATE() AND post_type = %s
                """
                cursor.execute(query, (post_type,))
            else:
                query = """
                SELECT COUNT(*) FROM posts 
                WHERE DATE(timestamp) = CURDATE()
                """
                cursor.execute(query)
            
            count = cursor.fetchone()[0]
            return count
            
        except Error as e:
            self.logger.error(f"Error getting post count: {e}")
            return 0
    
    def get_last_post_time(self):
        """Get the timestamp of the last post made today"""
        try:
            cursor = self.connection.cursor()
            
            query = """
            SELECT timestamp FROM posts 
            WHERE DATE(timestamp) = CURDATE() 
            ORDER BY timestamp DESC 
            LIMIT 1
            """
            
            cursor.execute(query)
            result = cursor.fetchone()
            
            if result:
                return result[0]
            return None
            
        except Error as e:
            self.logger.error(f"Error getting last post time: {e}")
            return None 