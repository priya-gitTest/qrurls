"""
QRURLs: A Python package for generating QR codes and shortening URLs
"""

__version__ = "0.1.0"
__author__ = "Priyanka O"
__email__ = "priyankaoe@gmail.com"

from .qr_generator import QRGenerator
from .url_shortener import URLShortener
from .core import QRURLs

__all__ = ['QRGenerator', 'URLShortener', 'QRURLs']