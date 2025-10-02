"""
# QRURLs

A Python package for generating QR codes and shortening URLs using open source services.

## Features

- Generate QR codes for any URL
- Shorten URLs using multiple open source services (TinyURL, is.gd, v.gd)
- Combine both: shorten URL and generate QR code in one step
- Save QR codes as images or get them as objects
- Simple, intuitive API

## Installation

```bash
pip install qrurls
```

Or with **uv** (faster):
```bash
uv pip install qrurls
```

## Quick Start

```python
from qrurls import QRURLs

# Create instance
qrurls = QRURLs(service='tinyurl')

# Shorten URL and generate QR code
short_url, qr_image = qrurls.process(
    'https://www.example.com/very/long/url',
    output_path='qr_code.png'
)

print(f"Shortened URL: {short_url}")
```
## Interactive Jupyter Notebook UI

For a user-friendly interface, use the included Jupyter notebook:

```bash
# Install with notebook support
pip install qrurls[notebook]
# or with uv:
uv pip install qrurls[notebook]

# Launch Jupyter
jupyter notebook qrurls_interactive.ipynb
```

The notebook provides:
- 🎨 Interactive widgets for all options
- 📱 Live QR code preview
- 💾 Automatic file saving with timestamps
- 🔗 Clickable shortened URLs
- 📊 Batch processing examples

## Usage Examples

### Just Shorten a URL

```python
from qrurls import URLShortener

shortener = URLShortener(service='isgd')
short_url = shortener.shorten('https://www.example.com/long/url')
print(short_url)
```

### Just Generate a QR Code

```python
from qrurls import QRGenerator

qr_gen = QRGenerator(box_size=10, border=4)
qr_gen.generate('https://example.com', output_path='qr.png')
```

### Combined Functionality

```python
from qrurls import QRURLs

# Initialize with preferred service
qrurls = QRURLs(service='vgd', box_size=10, border=4)

# Shorten and create QR code
short_url, qr_img = qrurls.process(
    'https://www.example.com',
    output_path='output_qr.png'
)

# Or use separately
short_url = qrurls.shorten_only('https://example.com')
qr_img = qrurls.qr_only('https://example.com', 'qr.png')
```

## Available Services

- `tinyurl` - TinyURL (default)
- `isgd` - is.gd
- `vgd` - v.gd

## Requirements

- Python 3.7+
- qrcode[pil]
- requests
- Pillow

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## Development & Publishing with uv (Recommended)

**uv** is a blazingly fast Python package manager written in Rust. Here's how to use it:

### Install uv
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### Development Workflow with uv

```bash
# Create a new project (if starting from scratch)
uv init qrurls
cd qrurls

# Add dependencies
uv add "qrcode[pil]>=7.3.1" "requests>=2.25.0" "Pillow>=8.0.0"

# Add dev dependencies
uv add --dev pytest pytest-cov black flake8

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install the package in editable mode
uv pip install -e .

# Run tests
uv run pytest

# Format code
uv run black .

# Run linting
uv run flake8
```

### Building with uv

```bash
# Build the package (uv uses hatchling/setuptools automatically)
uv build

# This creates:
# - dist/qrurls-0.1.0-py3-none-any.whl
# - dist/qrurls-0.1.0.tar.gz
```

### Publishing to PyPI with uv

```bash
# Install twine if needed
uv pip install twine

# Upload to TestPyPI first (recommended)
uv run twine upload --repository testpypi dist/*

# Test installation from TestPyPI
uv pip install --index-url https://test.pypi.org/simple/ qrurls

# If everything works, upload to real PyPI
uv run twine upload dist/*
```

### Why use uv?

- ⚡ **10-100x faster** than pip
- 🔒 **Deterministic** - Generates lockfiles automatically
- 🎯 **Simple** - One tool for everything
- 🦀 **Modern** - Written in Rust for performance
- 🔄 **Compatible** - Works with existing pip/PyPI packages

### Traditional Method (without uv)

If you prefer traditional tools:

```bash
# Install build tools
pip install build twine

# Build
python -m build

# Upload to PyPI
twine upload dist/*
```

Both methods work! uv is just faster and more modern.
"""