"""Tests for custom exceptions"""

from qrurls.exceptions import InvalidURLError, QRUrlsError, ShorteningError


def test_shortening_error_is_qrurls_error():
    assert issubclass(ShorteningError, QRUrlsError)


def test_invalid_url_error_is_qrurls_error():
    assert issubclass(InvalidURLError, QRUrlsError)


def test_qrurls_error_is_exception():
    assert issubclass(QRUrlsError, Exception)


def test_shortening_error_message():
    err = ShorteningError("test message")
    assert str(err) == "test message"


def test_invalid_url_error_message():
    err = InvalidURLError("bad url")
    assert str(err) == "bad url"
