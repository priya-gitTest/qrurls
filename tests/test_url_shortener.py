"""Tests for URLShortener"""

from unittest.mock import MagicMock, patch

import pytest
import requests

from qrurls import URLShortener
from qrurls.exceptions import InvalidURLError, ShorteningError

SAMPLE_URL = "https://www.example.com/path?query=1&other=2"
SHORT_URL = "https://tinyurl.com/abc123"


class TestInit:
    @pytest.mark.parametrize("service", ["tinyurl", "isgd", "vgd"])
    def test_valid_services(self, service):
        shortener = URLShortener(service=service)
        assert shortener.service == service

    def test_case_insensitive(self):
        shortener = URLShortener(service="TinyURL")
        assert shortener.service == "tinyurl"

    def test_invalid_service_raises(self):
        with pytest.raises(ValueError, match="Service must be one of"):
            URLShortener(service="badservice")


class TestValidateURL:
    def test_valid_url(self):
        URLShortener._validate_url("https://example.com")

    def test_missing_scheme(self):
        with pytest.raises(InvalidURLError, match="Invalid URL"):
            URLShortener._validate_url("example.com")

    def test_missing_netloc(self):
        with pytest.raises(InvalidURLError, match="Invalid URL"):
            URLShortener._validate_url("not-a-url")

    def test_empty_string(self):
        with pytest.raises(InvalidURLError, match="Invalid URL"):
            URLShortener._validate_url("")


class TestShortenTinyURL:
    @patch("qrurls.url_shortener.requests.get")
    def test_success(self, mock_get, tinyurl_shortener):
        mock_response = MagicMock()
        mock_response.text = "  https://tinyurl.com/abc123  \n"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = tinyurl_shortener.shorten(SAMPLE_URL)
        assert result == "https://tinyurl.com/abc123"
        mock_get.assert_called_once()

    @patch("qrurls.url_shortener.requests.get")
    def test_uses_params_not_fstring(self, mock_get, tinyurl_shortener):
        """Verify URL is passed via params dict, not interpolated into the URL"""
        mock_response = MagicMock()
        mock_response.text = SHORT_URL
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        tinyurl_shortener.shorten(SAMPLE_URL)
        _, kwargs = mock_get.call_args
        assert "params" in kwargs
        assert kwargs["params"]["url"] == SAMPLE_URL

    @patch("qrurls.url_shortener.requests.get")
    def test_network_error(self, mock_get, tinyurl_shortener):
        mock_get.side_effect = requests.ConnectionError("connection failed")
        with pytest.raises(ShorteningError, match="TinyURL"):
            tinyurl_shortener.shorten(SAMPLE_URL)

    @patch("qrurls.url_shortener.requests.get")
    def test_http_error(self, mock_get, tinyurl_shortener):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("500")
        mock_get.return_value = mock_response
        with pytest.raises(ShorteningError, match="TinyURL"):
            tinyurl_shortener.shorten(SAMPLE_URL)


class TestShortenIsgd:
    @patch("qrurls.url_shortener.requests.get")
    def test_success(self, mock_get, isgd_shortener):
        mock_response = MagicMock()
        mock_response.text = "https://is.gd/abc123"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = isgd_shortener.shorten(SAMPLE_URL)
        assert result == "https://is.gd/abc123"

    @patch("qrurls.url_shortener.requests.get")
    def test_uses_params(self, mock_get, isgd_shortener):
        mock_response = MagicMock()
        mock_response.text = "https://is.gd/abc123"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        isgd_shortener.shorten(SAMPLE_URL)
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["format"] == "simple"
        assert kwargs["params"]["url"] == SAMPLE_URL

    @patch("qrurls.url_shortener.requests.get")
    def test_network_error(self, mock_get, isgd_shortener):
        mock_get.side_effect = requests.ConnectionError()
        with pytest.raises(ShorteningError, match="is.gd"):
            isgd_shortener.shorten(SAMPLE_URL)


class TestShortenVgd:
    @patch("qrurls.url_shortener.requests.get")
    def test_success(self, mock_get, vgd_shortener):
        mock_response = MagicMock()
        mock_response.text = "https://v.gd/abc123"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = vgd_shortener.shorten(SAMPLE_URL)
        assert result == "https://v.gd/abc123"

    @patch("qrurls.url_shortener.requests.get")
    def test_network_error(self, mock_get, vgd_shortener):
        mock_get.side_effect = requests.ConnectionError()
        with pytest.raises(ShorteningError, match="v.gd"):
            vgd_shortener.shorten(SAMPLE_URL)


class TestShortenValidation:
    def test_invalid_url_raises(self, tinyurl_shortener):
        with pytest.raises(InvalidURLError):
            tinyurl_shortener.shorten("not-a-url")

    def test_empty_url_raises(self, tinyurl_shortener):
        with pytest.raises(InvalidURLError):
            tinyurl_shortener.shorten("")
