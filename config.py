import os
import sys
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        pass  # Fallback if dotenv is not available

# Load environment variables
# Check if running in daemon mode and load .env.production
if '--daemon' in sys.argv:
    load_dotenv('.env.production')
else:
    load_dotenv()

class Config:
    """Configuration class for the Automated Daily Poster Bot"""
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_NAME = os.getenv('DB_NAME', 'autopost_db')
    DB_USER = os.getenv('DB_USER', 'root1')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # API Configuration - RecentHPost API
    API_ENDPOINT = os.getenv('API_ENDPOINT', 'http://example.com/posts')
    API_KEY = os.getenv('API_KEY', '****************')
    
    # Post Configuration
    USER_ID = int(os.getenv('USER_ID', '1'))
    CATEGORY_ID = int(os.getenv('CATEGORY_ID', '1'))
    STATE = os.getenv('STATE', 'California')
    CITY = os.getenv('CITY', 'San Francisco')
    DEVICE = os.getenv('DEVICE', 'Python Bot 1.0')
    COUNTRIES_ISO = os.getenv('COUNTRIES_ISO', 'US').split(',')  # Can be multiple countries
    
    # Bot Configuration
    TIMEZONE = os.getenv('TIMEZONE', 'UTC')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Content API Sources (random internet APIs)
    CONTENT_APIS = [
        {
            'name': 'Quotes API',
            'url': 'https://api.quotable.io/random',
            'content_key': 'content',
            'author_key': 'author',
            'title_key': None  # No title available
        },
        {
            'name': 'Joke API',
            'url': 'https://official-joke-api.appspot.com/random_joke',
            'content_key': 'setup',
            'punchline_key': 'punchline',
            'title_key': None  # No title available
        },
        {
            'name': 'Advice API',
            'url': 'https://api.adviceslip.com/advice',
            'content_key': 'slip.advice',
            'title_key': None  # No title available
        },
        {
            'name': 'Useless Facts API',
            'url': 'https://uselessfacts.jsph.pl/api/v2/facts/random',
            'content_key': 'text',
            'title_key': None  # No title available
        },
        {
            'name': 'Dog Facts API',
            'url': 'https://dog-api.kinduff.com/api/facts',
            'content_key': 'facts.0',
            'title_key': None  # No title available
        },
        {
            'name': 'Random Word API',
            'url': 'https://random-word-api.herokuapp.com/word',
            'content_key': '0',
            'title_key': None  # No title available
        },
        {
            'name': 'Bored API',
            'url': 'https://www.boredapi.com/api/activity',
            'content_key': 'activity',
            'title_key': 'type'
        }
    ]
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present"""
        required_fields = [
            'API_ENDPOINT', 'API_KEY', 'USER_ID', 'CATEGORY_ID',
            'DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not getattr(cls, field):
                missing_fields.append(field)
        
        if missing_fields:
            raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")
        
        return True 