"""Tests for CLI"""

from unittest.mock import patch

from qrurls.cli import build_parser, main

SAMPLE_URL = "https://www.example.com"
SHORT_URL = "https://tinyurl.com/abc123"


class TestBuildParser:
    def test_url_required(self):
        parser = build_parser()
        args = parser.parse_args([SAMPLE_URL])
        assert args.url == SAMPLE_URL

    def test_defaults(self):
        parser = build_parser()
        args = parser.parse_args([SAMPLE_URL])
        assert args.service == "tinyurl"
        assert args.box_size == 10
        assert args.border == 4
        assert args.output is None
        assert args.shorten_only is False
        assert args.qr_only is False

    def test_all_options(self):
        parser = build_parser()
        args = parser.parse_args(
            [SAMPLE_URL, "-s", "isgd", "-o", "out.png", "--box-size", "5", "--border", "2"]
        )
        assert args.service == "isgd"
        assert args.output == "out.png"
        assert args.box_size == 5
        assert args.border == 2

    def test_shorten_only_flag(self):
        parser = build_parser()
        args = parser.parse_args([SAMPLE_URL, "--shorten-only"])
        assert args.shorten_only is True

    def test_qr_only_flag(self):
        parser = build_parser()
        args = parser.parse_args([SAMPLE_URL, "--qr-only"])
        assert args.qr_only is True

    def test_no_qr_alias(self):
        parser = build_parser()
        args = parser.parse_args([SAMPLE_URL, "--no-qr"])
        assert args.no_qr is True


class TestMainShortenOnly:
    @patch("qrurls.cli.QRURLs")
    def test_prints_short_url(self, mock_cls, capsys):
        mock_instance = mock_cls.return_value
        mock_instance.shorten_only.return_value = SHORT_URL

        result = main([SAMPLE_URL, "--shorten-only"])

        assert result == 0
        captured = capsys.readouterr()
        assert SHORT_URL in captured.out
        mock_instance.shorten_only.assert_called_once_with(SAMPLE_URL)

    @patch("qrurls.cli.QRURLs")
    def test_no_qr_alias_works(self, mock_cls, capsys):
        mock_instance = mock_cls.return_value
        mock_instance.shorten_only.return_value = SHORT_URL

        result = main([SAMPLE_URL, "--no-qr"])

        assert result == 0
        captured = capsys.readouterr()
        assert SHORT_URL in captured.out


class TestMainQROnly:
    @patch("qrurls.cli.QRURLs")
    def test_generates_qr_and_prints_path(self, mock_cls, capsys):
        mock_instance = mock_cls.return_value
        mock_instance.qr_only.return_value = "qr_20260315.png"
        mock_instance.qr_generator.print_ascii.return_value = None

        result = main([SAMPLE_URL, "--qr-only"])

        assert result == 0
        captured = capsys.readouterr()
        assert "qr_20260315.png" in captured.out
        mock_instance.qr_only.assert_called_once_with(SAMPLE_URL, None)

    @patch("qrurls.cli.QRURLs")
    def test_custom_output(self, mock_cls, capsys):
        mock_instance = mock_cls.return_value
        mock_instance.qr_only.return_value = "custom.png"
        mock_instance.qr_generator.print_ascii.return_value = None

        result = main([SAMPLE_URL, "--qr-only", "-o", "custom.png"])

        assert result == 0
        mock_instance.qr_only.assert_called_once_with(SAMPLE_URL, "custom.png")


class TestMainBoth:
    @patch("qrurls.cli.QRURLs")
    def test_shortens_and_generates_qr(self, mock_cls, capsys):
        mock_instance = mock_cls.return_value
        mock_instance.process.return_value = (SHORT_URL, "qr_out.png")
        mock_instance.qr_generator.print_ascii.return_value = None

        result = main([SAMPLE_URL])

        assert result == 0
        captured = capsys.readouterr()
        assert SHORT_URL in captured.out
        assert "qr_out.png" in captured.out
        mock_instance.process.assert_called_once_with(SAMPLE_URL, None)

    @patch("qrurls.cli.QRURLs")
    def test_passes_service_and_options(self, mock_cls):
        mock_instance = mock_cls.return_value
        mock_instance.process.return_value = (SHORT_URL, "out.png")
        mock_instance.qr_generator.print_ascii.return_value = None

        main([SAMPLE_URL, "-s", "isgd", "--box-size", "5", "--border", "2"])

        mock_cls.assert_called_once_with(service="isgd", box_size=5, border=2)


class TestMainErrors:
    @patch("qrurls.cli.QRURLs")
    def test_invalid_url_returns_1(self, mock_cls, capsys):
        from qrurls.exceptions import InvalidURLError

        mock_instance = mock_cls.return_value
        mock_instance.shorten_only.side_effect = InvalidURLError("Invalid URL: bad")

        result = main(["bad", "--shorten-only"])

        assert result == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    @patch("qrurls.cli.QRURLs")
    def test_shortening_error_returns_1(self, mock_cls, capsys):
        from qrurls.exceptions import ShorteningError

        mock_instance = mock_cls.return_value
        mock_instance.shorten_only.side_effect = ShorteningError("API down")

        result = main([SAMPLE_URL, "--shorten-only"])

        assert result == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
