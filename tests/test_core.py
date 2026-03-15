"""Tests for QRURLs (core)"""

import re
from unittest.mock import patch

from qrurls import QRURLs

SAMPLE_URL = "https://www.example.com/path?query=1&other=2"
SHORT_URL = "https://tinyurl.com/abc123"


class TestInit:
    def test_default_params(self):
        q = QRURLs()
        assert q.url_shortener.service == "tinyurl"
        assert q.qr_generator.box_size == 10
        assert q.qr_generator.border == 4

    def test_custom_params(self):
        q = QRURLs(service="isgd", box_size=5, border=2)
        assert q.url_shortener.service == "isgd"
        assert q.qr_generator.box_size == 5
        assert q.qr_generator.border == 2


class TestGenerateFilename:
    def test_format(self, qrurls_instance):
        filename = qrurls_instance._generate_filename()
        assert re.match(r"qr_\d{14}\.png", filename)

    def test_custom_prefix_extension(self, qrurls_instance):
        filename = qrurls_instance._generate_filename(prefix="test", extension="svg")
        assert re.match(r"test_\d{14}\.svg", filename)


class TestProcess:
    @patch("qrurls.core.QRGenerator.generate")
    @patch("qrurls.core.URLShortener.shorten")
    def test_returns_short_url_and_path(self, mock_shorten, mock_generate, qrurls_instance):
        mock_shorten.return_value = SHORT_URL
        mock_generate.return_value = None

        short_url, path = qrurls_instance.process(SAMPLE_URL, "out.png")
        assert short_url == SHORT_URL
        assert path == "out.png"
        mock_shorten.assert_called_once_with(SAMPLE_URL)
        mock_generate.assert_called_once_with(SHORT_URL, "out.png")

    @patch("qrurls.core.QRGenerator.generate")
    @patch("qrurls.core.URLShortener.shorten")
    def test_auto_generates_filename(self, mock_shorten, mock_generate, qrurls_instance):
        mock_shorten.return_value = SHORT_URL
        mock_generate.return_value = None

        short_url, path = qrurls_instance.process(SAMPLE_URL)
        assert short_url == SHORT_URL
        assert re.match(r"qr_\d{14}\.png", path)

    @patch("qrurls.core.QRGenerator.generate")
    @patch("qrurls.core.URLShortener.shorten")
    def test_generates_qr_for_shortened_url(self, mock_shorten, mock_generate, qrurls_instance):
        mock_shorten.return_value = SHORT_URL
        mock_generate.return_value = None

        qrurls_instance.process(SAMPLE_URL, "out.png")
        # QR should be generated for the shortened URL, not the original
        mock_generate.assert_called_once_with(SHORT_URL, "out.png")


class TestShortenOnly:
    @patch("qrurls.core.URLShortener.shorten")
    def test_delegates_to_shortener(self, mock_shorten, qrurls_instance):
        mock_shorten.return_value = SHORT_URL
        result = qrurls_instance.shorten_only(SAMPLE_URL)
        assert result == SHORT_URL
        mock_shorten.assert_called_once_with(SAMPLE_URL)


class TestQROnly:
    @patch("qrurls.core.QRGenerator.generate")
    def test_returns_path(self, mock_generate, qrurls_instance):
        mock_generate.return_value = None
        path = qrurls_instance.qr_only(SAMPLE_URL, "custom.png")
        assert path == "custom.png"
        mock_generate.assert_called_once_with(SAMPLE_URL, "custom.png")

    @patch("qrurls.core.QRGenerator.generate")
    def test_auto_generates_filename(self, mock_generate, qrurls_instance):
        mock_generate.return_value = None
        path = qrurls_instance.qr_only(SAMPLE_URL)
        assert re.match(r"qr_\d{14}\.png", path)

    @patch("qrurls.core.QRGenerator.generate")
    def test_uses_original_url_not_shortened(self, mock_generate, qrurls_instance):
        mock_generate.return_value = None
        qrurls_instance.qr_only(SAMPLE_URL, "out.png")
        # qr_only should use the original URL, not shorten it
        mock_generate.assert_called_once_with(SAMPLE_URL, "out.png")
