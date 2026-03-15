"""
Custom exceptions for the qrurls package
"""


class QRUrlsError(Exception):
    """Base exception for qrurls package."""

    pass


class ShorteningError(QRUrlsError):
    """Raised when URL shortening fails."""

    pass


class InvalidURLError(QRUrlsError):
    """Raised when an invalid URL is provided."""

    pass
