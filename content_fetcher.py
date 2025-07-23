import requests
import random
import logging
from typing import Dict, Optional
from config import Config

class ContentFetcher:
    """Fetches content from various random internet APIs"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AutomatedPosterBot/1.0'
        })
    
    def get_nested_value(self, data: Dict, key_path: str) -> Optional[str]:
        """Get nested dictionary value using dot notation"""
        keys = key_path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return str(current) if current is not None else None
    
    def fetch_content(self) -> Dict:
        """Fetch content from multiple APIs, trying each one until success"""
        # Shuffle the APIs to try them in random order
        apis_to_try = Config.CONTENT_APIS.copy()
        random.shuffle(apis_to_try)
        
        for api_config in apis_to_try:
            try:
                self.logger.info(f"Trying to fetch content from: {api_config['name']}")
                
                response = self.session.get(api_config['url'], timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                # Extract content based on API configuration
                content = self.get_nested_value(data, api_config['content_key'])
                
                if not content:
                    self.logger.warning(f"Could not extract content from {api_config['name']}")
                    continue
                
                # Build the post content
                post_content = content
                
                # Add author if available (for quotes)
                if 'author_key' in api_config:
                    author = self.get_nested_value(data, api_config['author_key'])
                    if author:
                        post_content += f" - {author}"
                
                # Add punchline if available (for jokes)
                if 'punchline_key' in api_config:
                    punchline = self.get_nested_value(data, api_config['punchline_key'])
                    if punchline:
                        post_content += f"\n{punchline}"
                
                # Extract title if available
                title = None
                if 'title_key' in api_config and api_config['title_key']:
                    title = self.get_nested_value(data, api_config['title_key'])
                
                self.logger.info(f"Successfully fetched content from: {api_config['name']}")
                return {
                    'content': post_content,
                    'title': title,
                    'api_name': api_config['name'],
                    'api_url': api_config['url']
                }
                
            except requests.RequestException as e:
                self.logger.warning(f"Request error fetching from {api_config['name']}: {e}")
                continue
            except (KeyError, ValueError, TypeError) as e:
                self.logger.warning(f"Data parsing error from {api_config['name']}: {e}")
                continue
            except Exception as e:
                self.logger.warning(f"Unexpected error fetching from {api_config['name']}: {e}")
                continue
        
        # If all APIs failed, raise an exception to trigger fallback
        raise Exception("All content APIs failed")
    
    def get_fallback_content(self) -> Dict:
        """Get fallback content when all APIs fail"""
        # Extensive collection of diverse fallback messages
        fallback_messages = [
            # Motivational quotes
            "The only way to do great work is to love what you do. 💪",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. 🚀",
            "The future belongs to those who believe in the beauty of their dreams. 🌈",
            "Life is what happens while you're busy making other plans. ✨",
            "Sometimes the best content is the simplest content. Have a great day! 🌟",
            
            # Wisdom and philosophy
            "The journey of a thousand miles begins with one step. 🚶‍♂️",
            "What you get by achieving your goals is not as important as what you become by achieving your goals. 🎯",
            "The mind is everything. What you think you become. 🧠",
            "Happiness is not something ready-made. It comes from your own actions. 😊",
            "Peace comes from within. Do not seek it without. 🕊️",
            
            # Life advice
            "Take life day by day and be grateful for the little things. 🙏",
            "Don't wait for the perfect moment, take the moment and make it perfect. ⏰",
            "Your time is limited, don't waste it living someone else's life. ⏳",
            "The best way to predict the future is to create it. 🔮",
            "Dream big, work hard, stay focused, and surround yourself with good people. 👥",
            
            # Positive affirmations
            "You are capable of amazing things. Believe in yourself! 💫",
            "Every day is a new beginning. Take a deep breath and start again. 🌅",
            "You have the power to change your story. 📖",
            "Your potential is limitless. Keep pushing forward! 🚀",
            "Today is your day to shine! ✨",
            
            # Humor and light-hearted
            "Coffee: because adulting is hard. ☕",
            "Life is short, make it sweet! 🍭",
            "Dance like nobody's watching, sing like nobody's listening. 🎵",
            "Laughter is the best medicine. Keep smiling! 😄",
            "Life is better when you're laughing. 😂",
            
            # Technology and modern life
            "In a world full of trends, remain a classic. 📱",
            "Technology is best when it brings people together. 🤝",
            "Innovation distinguishes between a leader and a follower. 💡",
            "The internet is not just one thing, it's a collection of things. 🌐",
            "Digital age, analog heart. ❤️",
            
            # Nature and environment
            "Nature does not hurry, yet everything is accomplished. 🌿",
            "The earth has music for those who listen. 🎶",
            "In every walk with nature, one receives far more than he seeks. 🌲",
            "Look deep into nature, and then you will understand everything better. 🔍",
            "The beauty of nature is that it's free. 🌸",
            
            # Creativity and art
            "Creativity is intelligence having fun. 🎨",
            "Art enables us to find ourselves and lose ourselves at the same time. 🖼️",
            "Every artist was first an amateur. 🎭",
            "Creativity takes courage. 💪",
            "Art is not what you see, but what you make others see. 👁️",
            
            # Learning and growth
            "Education is not preparation for life; education is life itself. 📚",
            "The more you learn, the more you earn. 💰",
            "Knowledge is power, but enthusiasm pulls the switch. ⚡",
            "Learning never exhausts the mind. 🧠",
            "The capacity to learn is a gift; the ability to learn is a skill. 🎁",
            
            # Friendship and relationships
            "Friendship is born at that moment when one person says to another, 'What! You too?' 👥",
            "A real friend is one who walks in when the rest of the world walks out. 🤗",
            "Friends are the family we choose for ourselves. 👨‍👩‍👧‍👦",
            "The language of friendship is not words but meanings. 💬",
            "Good friends are like stars. You don't always see them, but you know they're always there. ⭐"
        ]
        
        return {
            'content': random.choice(fallback_messages),
            'title': None,  # No title for fallback content
            'api_name': 'Fallback',
            'api_url': 'internal'
        } 