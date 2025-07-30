"""
Configuration settings for the Automated Daily Poster Bot.

This module contains all configuration settings including database,
API, and bot configuration with environment variable support.
"""

import os
import sys
from typing import List, Dict, Any
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:

    def load_dotenv():
        pass  # Fallback if dotenv is not available


# Load environment variables
# Check if running in daemon mode and load .env.production
if "--daemon" in sys.argv:
    load_dotenv(".env.production")
else:
    load_dotenv()


class DatabaseConfig:
    """Database configuration settings"""

    HOST = os.getenv("DB_HOST", "127.0.0.1")
    PORT = int(os.getenv("DB_PORT", 3306))
    NAME = os.getenv("DB_NAME", "autopost_db")
    USER = os.getenv("DB_USER", "root1")
    PASSWORD = os.getenv("DB_PASSWORD", "")


class APIConfig:
    """API configuration settings for RecentHPost API"""

    ENDPOINT = os.getenv("API_ENDPOINT", "http://example.com/posts")
    KEY = os.getenv("API_KEY", "****************")

    # Post configuration
    USER_ID = int(os.getenv("USER_ID", "1"))
    CATEGORY_ID = int(os.getenv("CATEGORY_ID", "1"))
    STATE = os.getenv("STATE", "California")
    CITY = os.getenv("CITY", "San Francisco")
    DEVICE = os.getenv("DEVICE", "Python Bot 1.0")
    COUNTRIES_ISO = os.getenv("COUNTRIES_ISO", "US").split(
        ","
    )  # Can be multiple countries


class BotConfig:
    """Bot configuration settings"""

    TIMEZONE = os.getenv("TIMEZONE", "UTC")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "autopost_bot.log")


class ContentAPIConfig:
    """Content API sources configuration"""

    SOURCES = [
        {
            "name": "Quotes API",
            "url": "https://api.quotable.io/random",
            "content_key": "content",
            "author_key": "author",
            "title_key": None,  # No title available
        },
        {
            "name": "Joke API",
            "url": "https://official-joke-api.appspot.com/random_joke",
            "content_key": "setup",
            "punchline_key": "punchline",
            "title_key": None,  # No title available
        },
        {
            "name": "Advice API",
            "url": "https://api.adviceslip.com/advice",
            "content_key": "slip.advice",
            "title_key": None,  # No title available
        },
        {
            "name": "Useless Facts API",
            "url": "https://uselessfacts.jsph.pl/api/v2/facts/random",
            "content_key": "text",
            "title_key": None,  # No title available
        },
        {
            "name": "Dog Facts API",
            "url": "https://dog-api.kinduff.com/api/facts",
            "content_key": "facts.0",
            "title_key": None,  # No title available
        },
        {
            "name": "Random Word API",
            "url": "https://random-word-api.herokuapp.com/word",
            "content_key": "0",
            "title_key": None,  # No title available
        },
        {
            "name": "Bored API",
            "url": "https://www.boredapi.com/api/activity",
            "content_key": "activity",
            "title_key": "type",
        },
    ]


class Config:
    """Main configuration class that aggregates all settings"""

    # Import all configuration classes
    Database = DatabaseConfig
    API = APIConfig
    Bot = BotConfig
    ContentAPI = ContentAPIConfig

    # Backward compatibility aliases
    DB_HOST = DatabaseConfig.HOST
    DB_PORT = DatabaseConfig.PORT
    DB_NAME = DatabaseConfig.NAME
    DB_USER = DatabaseConfig.USER
    DB_PASSWORD = DatabaseConfig.PASSWORD

    API_ENDPOINT = APIConfig.ENDPOINT
    API_KEY = APIConfig.KEY
    USER_ID = APIConfig.USER_ID
    CATEGORY_ID = APIConfig.CATEGORY_ID
    STATE = APIConfig.STATE
    CITY = APIConfig.CITY
    DEVICE = APIConfig.DEVICE
    COUNTRIES_ISO = APIConfig.COUNTRIES_ISO

    TIMEZONE = BotConfig.TIMEZONE
    LOG_LEVEL = BotConfig.LOG_LEVEL

    CONTENT_APIS = ContentAPIConfig.SOURCES

    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configuration is present"""
        required_fields = [
            "API_ENDPOINT",
            "API_KEY",
            "USER_ID",
            "CATEGORY_ID",
            "DB_HOST",
            "DB_NAME",
            "DB_USER",
            "DB_PASSWORD",
        ]

        missing_fields = []
        for field in required_fields:
            if not getattr(cls, field):
                missing_fields.append(field)

        if missing_fields:
            print(
                f"❌ Missing required configuration fields: {', '.join(missing_fields)}"
            )
            print("Please check your .env file or environment variables.")
            return False

        return True

    @classmethod
    def get_project_root(cls) -> Path:
        """Get the project root directory"""
        return Path(__file__).parent.parent.parent

    @classmethod
    def get_log_file_path(cls) -> Path:
        """Get the log file path"""
        return cls.get_project_root() / cls.Bot.LOG_FILE
