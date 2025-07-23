import requests
import logging
import time
from typing import Optional, Dict, List
from config import Config

class APIClient:
    """Handles authentication and posting to the RecentHPost API"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'AutomatedPosterBot/1.0',
            'x-api-key': Config.API_KEY
        })
    
    def post_content(self, content: str, title: str = None, hashtags: List[str] = None, 
                    media_urls: List[str] = None) -> Dict:
        """Post content to the RecentHPost API using multipart/form-data"""
        try:
            self.logger.info("Posting content to RecentHPost API...")
            
            # Prepare form data
            form_data = {
                'title': title or "", #f"Auto Post - {int(time.time())}",
                'category_id': str(Config.CATEGORY_ID),
                'state': Config.STATE,
                'device': Config.DEVICE,
                'city': Config.CITY,
                'user_id': str(Config.USER_ID),
                'content': content
            }
            
            # Add countries_iso array
            for country in Config.COUNTRIES_ISO:
                form_data[f'countries_iso[]'] = country
            
            # Add hashtags array (can be empty)
            if hashtags:
                for hashtag in hashtags:
                    form_data[f'hashtags[]'] = hashtag
            else:
                # Add empty hashtag if none provided
                form_data[f'hashtags[]'] = ''
            
            # Add media files URLs array (can be empty)
            if media_urls:
                for url in media_urls:
                    form_data[f'media_files_urls[]'] = url
            # else:
                # Add empty media URL if none provided
                # form_data[f'media_files_urls[]'] = ''
            
            # Make the POST request with multipart/form-data
            response = self.session.post(
                Config.API_ENDPOINT,
                data=form_data,  # This creates multipart/form-data
                timeout=30
            )
            
            response.raise_for_status()
            
            result = response.json() if response.content else {}
            self.logger.info("Content posted successfully")
            
            return {
                'success': True,
                'response': result,
                'status_code': response.status_code
            }
            
        except requests.RequestException as e:
            self.logger.error(f"Post request failed: {e}")
            print(e.response.content)
            return {
                'success': False,
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
        except Exception as e:
            self.logger.error(f"Unexpected error posting content: {e}")
            return {
                'success': False,
                'error': str(e),
                'status_code': None
            }
    
    def test_connection(self) -> bool:
        """Test the API connection and authentication using a simple ping"""
        try:
            self.logger.info("Testing RecentHPost API connection...")
            
            # Try a simple GET request to test connectivity
            # First, try to ping the base URL
            base_url = Config.API_ENDPOINT.rsplit('/', 1)[0]  # Remove '/posts' from endpoint
            
            # Try different ping endpoints
            ping_urls = [
                f"{base_url}/health",
                f"{base_url}/ping", 
                f"{base_url}/status",
                f"{base_url}/",
                Config.API_ENDPOINT  # Try the actual endpoint with GET
            ]
            
            for ping_url in ping_urls:
                try:
                    self.logger.info(f"Pinging: {ping_url}")
                    response = self.session.get(ping_url, timeout=10)
                    
                    # Accept any 2xx or 4xx response as "reachable"
                    if response.status_code < 500:
                        self.logger.info(f"API endpoint reachable: {ping_url} (Status: {response.status_code})")
                        return True
                    else:
                        self.logger.warning(f"API endpoint returned error: {ping_url} (Status: {response.status_code})")
                        
                except requests.RequestException as e:
                    self.logger.debug(f"Ping failed for {ping_url}: {e}")
                    continue
            
            # If all pings failed, try a HEAD request to the main endpoint
            try:
                self.logger.info(f"Trying HEAD request to: {Config.API_ENDPOINT}")
                response = self.session.head(Config.API_ENDPOINT, timeout=10)
                self.logger.info(f"API endpoint reachable via HEAD: {Config.API_ENDPOINT} (Status: {response.status_code})")
                return True
            except requests.RequestException as e:
                self.logger.debug(f"HEAD request failed: {e}")
            
            self.logger.error("All ping attempts failed - API endpoint not reachable")
            return False
                
        except Exception as e:
            self.logger.error(f"API connection test failed: {e}")
            return False 