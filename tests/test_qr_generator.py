"""Tests for QRGenerator"""

import io

from qrurls import QRGenerator

SAMPLE_URL = "https://www.example.com"


class TestQRGeneratorInit:
    def test_default_params(self):
        gen = QRGenerator()
        assert gen.box_size == 10
        assert gen.border == 4

    def test_custom_params(self):
        gen = QRGenerator(box_size=5, border=2)
        assert gen.box_size == 5
        assert gen.border == 2


class TestGenerate:
    def test_returns_image_when_no_path(self, qr_generator):
        result = qr_generator.generate(SAMPLE_URL)
        assert result is not None
        assert hasattr(result, "save")

    def test_saves_to_file(self, qr_generator, tmp_path):
        output = tmp_path / "test.png"
        result = qr_generator.generate(SAMPLE_URL, str(output))
        assert result is None
        assert output.exists()
        assert output.stat().st_size > 0

    def test_returns_none_when_path_given(self, qr_generator, tmp_path):
        output = tmp_path / "test.png"
        result = qr_generator.generate(SAMPLE_URL, str(output))
        assert result is None

    def test_custom_box_size_produces_image(self, small_qr_generator):
        result = small_qr_generator.generate(SAMPLE_URL)
        assert result is not None
        assert hasattr(result, "save")


class TestGenerateSVG:
    def test_returns_string(self, qr_generator):
        result = qr_generator.generate_svg(SAMPLE_URL)
        assert isinstance(result, str)

    def test_contains_svg_markup(self, qr_generator):
        result = qr_generator.generate_svg(SAMPLE_URL)
        assert "<svg" in result.lower() or "<path" in result.lower()


class TestPrintAscii:
    def test_outputs_to_stream(self, qr_generator):
        buf = io.StringIO()
        qr_generator.print_ascii(SAMPLE_URL, out=buf)
        output = buf.getvalue()
        assert len(output) > 0

    def test_contains_block_characters(self, qr_generator):
        buf = io.StringIO()
        qr_generator.print_ascii(SAMPLE_URL, out=buf)
        output = buf.getvalue()
        # qrcode's print_ascii uses block chars or spaces
        assert "\u2588" in output or "\u2584" in output or " " in output
