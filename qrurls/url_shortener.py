"""
URL shortening functionality using open source services
"""

from urllib.parse import urlparse

import requests

from .exceptions import InvalidURLError, ShorteningError


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

    def _validate_service(self) -> None:
        """Validate the selected service"""
        valid_services = ["tinyurl", "isgd", "vgd"]
        if self.service not in valid_services:
            raise ValueError(f"Service must be one of {valid_services}")

    @staticmethod
    def _validate_url(url: str) -> None:
        """Validate that the input is a proper URL"""
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise InvalidURLError(f"Invalid URL: {url}")

    def shorten(self, url: str) -> str:
        """
        Shorten a URL using the selected service

        Args:
            url: URL to shorten

        Returns:
            Shortened URL

        Raises:
            InvalidURLError: If the URL is not valid
            ShorteningError: If URL shortening fails
        """
        self._validate_url(url)

        if self.service == "tinyurl":
            return self._shorten_tinyurl(url)
        elif self.service == "isgd":
            return self._shorten_isgd(url)
        elif self.service == "vgd":
            return self._shorten_vgd(url)

        raise ValueError(f"Unknown service: {self.service}")

    def _shorten_tinyurl(self, url: str) -> str:
        """Shorten URL using TinyURL API"""
        try:
            response = requests.get(
                "http://tinyurl.com/api-create.php",
                params={"url": url},
                timeout=10,
            )
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            raise ShorteningError(f"Failed to shorten URL with TinyURL: {str(e)}")

    def _shorten_isgd(self, url: str) -> str:
        """Shorten URL using is.gd API"""
        try:
            response = requests.get(
                "https://is.gd/create.php",
                params={"format": "simple", "url": url},
                timeout=10,
            )
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            raise ShorteningError(f"Failed to shorten URL with is.gd: {str(e)}")

    def _shorten_vgd(self, url: str) -> str:
        """Shorten URL using v.gd API"""
        try:
            response = requests.get(
                "https://v.gd/create.php",
                params={"format": "simple", "url": url},
                timeout=10,
            )
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            raise ShorteningError(f"Failed to shorten URL with v.gd: {str(e)}")
