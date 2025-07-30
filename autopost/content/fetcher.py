"""
Content fetching module for the Automated Daily Poster Bot.

This module handles fetching content from various external APIs
and provides fallback content when APIs are unavailable.
"""

import requests
import logging
import random
from typing import Dict, List, Optional, Any
from requests.exceptions import RequestException

from ..config.settings import Config


class ContentFetcher:
    """Fetches content from various external APIs"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "AutomatedPosterBot/1.0"})

    def fetch_content(self) -> Dict[str, Any]:
        """Fetch content from a random API source"""
        # Shuffle the APIs to get random selection
        apis = Config.ContentAPI.SOURCES.copy()
        random.shuffle(apis)

        for api in apis:
            try:
                content_data = self._fetch_from_api(api)
                if content_data:
                    return content_data
            except Exception as e:
                self.logger.warning(f"Failed to fetch from {api['name']}: {e}")
                continue

        # If all APIs fail, return fallback content
        self.logger.warning("All content APIs failed, using fallback content")
        return self.get_fallback_content()

    def _fetch_from_api(self, api: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Fetch content from a specific API"""
        try:
            self.logger.info(f"Fetching content from {api['name']}...")

            response = self.session.get(api["url"], timeout=10)
            response.raise_for_status()

            data = response.json()

            # Extract content based on API configuration
            content = self._extract_content(data, api)
            title = self._extract_title(data, api)

            if not content:
                raise ValueError(f"No content found in {api['name']} response")

            # Clean and format content
            content = self._clean_content(content, api)

            return {
                "content": content,
                "title": title,
                "api_name": api["name"],
                "api_url": api["url"],
            }

        except Exception as e:
            self.logger.error(f"Error fetching from {api['name']}: {e}")
            return None

    def _extract_content(self, data: Dict, api: Dict[str, Any]) -> Optional[str]:
        """Extract content from API response based on configuration"""
        try:
            content_key = api["content_key"]

            # Handle nested keys (e.g., 'slip.advice')
            if "." in content_key:
                keys = content_key.split(".")
                value = data
                for key in keys:
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    else:
                        return None
                return str(value)
            else:
                return str(data.get(content_key, ""))

        except Exception as e:
            self.logger.error(f"Error extracting content from {api['name']}: {e}")
            return None

    def _extract_title(self, data: Dict, api: Dict[str, Any]) -> Optional[str]:
        """Extract title from API response if available"""
        try:
            title_key = api.get("title_key")
            if not title_key:
                return None

            # Handle nested keys
            if "." in title_key:
                keys = title_key.split(".")
                value = data
                for key in keys:
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    else:
                        return None
                return str(value)
            else:
                return str(data.get(title_key, ""))

        except Exception as e:
            self.logger.error(f"Error extracting title from {api['name']}: {e}")
            return None

    def _clean_content(self, content: str, api: Dict[str, Any]) -> str:
        """Clean and format content based on API type"""
        content = content.strip()

        # Handle special cases for different APIs
        if api["name"] == "Joke API":
            # For jokes, combine setup and punchline
            punchline_key = api.get("punchline_key")
            if punchline_key and punchline_key in api:
                # This would need to be handled in the main fetch method
                pass

        # Remove excessive whitespace
        content = " ".join(content.split())

        # Ensure content is not too long (Twitter-like limit)
        if len(content) > 280:
            content = content[:277] + "..."

        return content

    def get_fallback_content(self) -> Dict[str, Any]:
        """Get fallback content when all APIs fail"""
        fallback_content = [
            "Sometimes the best content is the simplest content. Keep it real! 🌟",
            "Life is what happens while you're busy making other plans. - John Lennon 📝",
            "The only way to do great work is to love what you do. - Steve Jobs 💼",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill 🎯",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt ✨",
            "Don't watch the clock; do what it does. Keep going. ⏰",
            "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt 🌅",
            "It always seems impossible until it's done. - Nelson Mandela 🏆",
            "The best way to predict the future is to create it. - Peter Drucker 🔮",
            "Dream big, work hard, stay focused, and surround yourself with good people. 🚀",
        ]

        content = random.choice(fallback_content)

        return {
            "content": content,
            "title": None,
            "api_name": "Fallback Content",
            "api_url": None,
        }

    def get_available_apis(self) -> List[Dict[str, Any]]:
        """Get list of available content APIs with their status"""
        available_apis = []

        for api in Config.ContentAPI.SOURCES:
            try:
                response = self.session.get(api["url"], timeout=5)
                status = "available" if response.status_code == 200 else "unavailable"
            except Exception:
                status = "unavailable"

            available_apis.append(
                {"name": api["name"], "url": api["url"], "status": status}
            )

        return available_apis

    def test_api_connection(self, api_name: str = None) -> Dict[str, Any]:
        """Test connection to content APIs"""
        results = {}

        if api_name:
            # Test specific API
            api = next(
                (a for a in Config.ContentAPI.SOURCES if a["name"] == api_name), None
            )
            if api:
                results[api_name] = self._test_single_api(api)
        else:
            # Test all APIs
            for api in Config.ContentAPI.SOURCES:
                results[api["name"]] = self._test_single_api(api)

        return results

    def _test_single_api(self, api: Dict[str, Any]) -> Dict[str, Any]:
        """Test a single API connection"""
        try:
            response = self.session.get(api["url"], timeout=10)

            if response.status_code == 200:
                data = response.json()
                content = self._extract_content(data, api)

                return {
                    "status": "available",
                    "response_time": response.elapsed.total_seconds(),
                    "content_sample": (
                        content[:100] + "..."
                        if content and len(content) > 100
                        else content
                    ),
                }
            else:
                return {
                    "status": "unavailable",
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}",
                }

        except Exception as e:
            return {"status": "error", "error": str(e)}
