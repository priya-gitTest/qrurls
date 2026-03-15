"""
Core functionality combining QR generation and URL shortening
"""

from datetime import datetime
from typing import Optional, Tuple

from .qr_generator import QRGenerator
from .url_shortener import URLShortener


class QRURLs:
    """Combined QR code generation and URL shortening"""

    def __init__(self, service: str = "tinyurl", box_size: int = 10, border: int = 4):
        """
        Initialize QRURLs

        Args:
            service: URL shortening service to use
            box_size: QR code box size
            border: QR code border size
        """
        self.qr_generator = QRGenerator(box_size=box_size, border=border)
        self.url_shortener = URLShortener(service=service)

    def _generate_filename(self, prefix: str = "qr", extension: str = "png") -> str:
        """
        Generate filename with timestamp

        Args:
            prefix: Filename prefix
            extension: File extension

        Returns:
            Filename in format: prefix_yyyymmddhhmmss.extension
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"

    def process(self, url: str, output_path: Optional[str] = None) -> Tuple[str, str]:
        """
        Shorten URL and generate QR code

        Args:
            url: Original URL
            output_path: Optional path to save QR code.
                If None, auto-generates filename with timestamp

        Returns:
            Tuple of (shortened_url, qr_image)
        """
        # Shorten the URL
        short_url = self.url_shortener.shorten(url)

        # Generate filename with timestamp if not provided
        if output_path is None:
            output_path = self._generate_filename()

        # Generate QR code for shortened URL
        self.qr_generator.generate(short_url, output_path)

        return short_url, output_path

    def shorten_only(self, url: str) -> str:
        """Shorten URL without generating QR code"""
        return self.url_shortener.shorten(url)

    def qr_only(self, url: str, output_path: Optional[str] = None) -> str:
        """
        Generate QR code without shortening URL

        Args:
            url: URL to encode
            output_path: Optional path to save QR code.
                If None, auto-generates filename with timestamp
        """
        if output_path is None:
            output_path = self._generate_filename()

        self.qr_generator.generate(url, output_path)
        return output_path
