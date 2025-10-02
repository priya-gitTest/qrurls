"""
URL shortening functionality using open source services
"""
import requests
from typing import Optional, Dict
import hashlib
import json


class URLShortener:
    """Shorten URLs using various open source services"""
    
    def __init__(self, service: str = "tinyurl"):
        """
        Initialize URL shortener
        
        Args:
            service: Service to use ('tinyurl', 'isgd', or 'vgd')
        """
        self.service = service.lower()
        self._validate_service()
    
    def _validate_service(self):
        """Validate the selected service"""
        valid_services = ['tinyurl', 'isgd', 'vgd']
        if self.service not in valid_services:
            raise ValueError(f"Service must be one of {valid_services}")
    
    def shorten(self, url: str) -> str:
        """
        Shorten a URL using the selected service
        
        Args:
            url: URL to shorten
            
        Returns:
            Shortened URL
            
        Raises:
            Exception: If URL shortening fails
        """
        if self.service == 'tinyurl':
            return self._shorten_tinyurl(url)
        elif self.service == 'isgd':
            return self._shorten_isgd(url)
        elif self.service == 'vgd':
            return self._shorten_vgd(url)
    
    def _shorten_tinyurl(self, url: str) -> str:
        """Shorten URL using TinyURL API"""
        api_url = f"http://tinyurl.com/api-create.php?url={url}"
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            raise Exception(f"Failed to shorten URL with TinyURL: {str(e)}")
    
    def _shorten_isgd(self, url: str) -> str:
        """Shorten URL using is.gd API"""
        api_url = f"https://is.gd/create.php?format=simple&url={url}"
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            raise Exception(f"Failed to shorten URL with is.gd: {str(e)}")
    
    def _shorten_vgd(self, url: str) -> str:
        """Shorten URL using v.gd API"""
        api_url = f"https://v.gd/create.php?format=simple&url={url}"
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            raise Exception(f"Failed to shorten URL with v.gd: {str(e)}")