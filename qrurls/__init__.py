"""
QRURLs: A Python package for generating QR codes and shortening URLs
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("qrurls")
except PackageNotFoundError:
    __version__ = "0.0.0"

__author__ = "Priyanka O"
__email__ = "priyankaoe@gmail.com"

from .core import QRURLs
from .exceptions import InvalidURLError, QRUrlsError, ShorteningError
from .qr_generator import QRGenerator
from .url_shortener import URLShortener

__all__ = [
    "QRGenerator",
    "URLShortener",
    "QRURLs",
    "QRUrlsError",
    "ShorteningError",
    "InvalidURLError",
]
