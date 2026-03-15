import pytest

from qrurls import QRGenerator, QRURLs, URLShortener

SAMPLE_URL = "https://www.example.com/path?query=1&other=2"
SHORT_URL = "https://tinyurl.com/abc123"


@pytest.fixture
def qr_generator():
    return QRGenerator(box_size=10, border=4)


@pytest.fixture
def small_qr_generator():
    return QRGenerator(box_size=5, border=2)


@pytest.fixture
def tinyurl_shortener():
    return URLShortener(service="tinyurl")


@pytest.fixture
def isgd_shortener():
    return URLShortener(service="isgd")


@pytest.fixture
def vgd_shortener():
    return URLShortener(service="vgd")


@pytest.fixture
def qrurls_instance():
    return QRURLs(service="tinyurl")
