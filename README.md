# QRURLs

A Python package for generating QR codes and shortening URLs using open source services.

<p align="center">
  <a href="https://tinyurl.com/2bve7rqv">
    <img src="assets/qrurls_demo.png" alt="QRURLs Demo — Shortened URL with QR Code" width="400">
  </a>
</p>

## Features

- Generate QR codes for any URL
- Shorten URLs using multiple open source services (TinyURL, is.gd, v.gd)
- Combine both: shorten URL and generate QR code in one step
- Command-line interface with ASCII QR display in terminal
- Save QR codes as PNG or SVG
- Interactive Jupyter notebook UI
- Hosted web app via Streamlit (no install needed)
- Simple, intuitive API

## Installation

[![PyPI](https://img.shields.io/pypi/v/qrurls)](https://pypi.org/project/qrurls/)

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
short_url, filepath = qrurls.process(
    'https://www.example.com/very/long/url',
    output_path='qr_code.png'
)

print(f"Shortened URL: {short_url}")
print(f"QR code saved to: {filepath}")
```

## Command-Line Interface

```bash
# Shorten URL + generate QR code (prints ASCII QR to terminal + saves PNG)
qrurls https://example.com/some/long/url

# Shorten only — prints the short URL
qrurls https://example.com/some/long/url --shorten-only

# QR code only — no URL shortening
qrurls https://example.com --qr-only

# Choose a service and output file
qrurls https://example.com -s isgd -o my_qr.png

# Customise QR appearance
qrurls https://example.com --box-size 5 --border 2
```

## Web App (No Install Needed)

Try QRURLs directly in your browser — no Python required:

<!-- TODO: replace with your actual Streamlit Cloud URL after deploying -->
**[Launch QRURLs Web App](https://qrurls.streamlit.app)**

Or run it locally:
```bash
pip install qrurls[streamlit]
streamlit run streamlit_app.py
```

## Interactive Jupyter Notebook UI

For a user-friendly interface, use the included Jupyter notebook:

```bash
# Install with notebook support
pip install qrurls[notebook]

# Launch Jupyter
jupyter notebook qrurls_interactive.ipynb
```

The notebook provides:
- Interactive widgets for all options
- Live QR code preview
- Automatic file saving with timestamps
- Clickable shortened URLs
- Batch processing examples

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
short_url, filepath = qrurls.process(
    'https://www.example.com',
    output_path='output_qr.png'
)

# Or use separately
short_url = qrurls.shorten_only('https://example.com')
filepath = qrurls.qr_only('https://example.com', 'qr.png')
```

## Available Services

- `tinyurl` - TinyURL (default)
- `isgd` - is.gd
- `vgd` - v.gd

## Requirements

- Python 3.9+
- qrcode[pil]
- requests
- Pillow

## Future Ideas

QR codes can encode more than just URLs — patient/specimen labels for labs, WiFi credentials, vCards, inventory tags, batch label generation from CSV, and more.

If you'd like to see any of these features, please **star the repo** and [open an issue](https://github.com/priya-gitTest/qrurls/issues) describing your use case!

## Citation

If you use QRURLs in your research or project, please cite it:

```bibtex
@software{priyanka_o_qrurls,
  author       = {Priyanka O},
  title        = {QRURLs},
  url          = {https://github.com/priya-gitTest/qrurls},
  license      = {MIT}
}
```

[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--6844--6493-green)](https://orcid.org/0000-0002-6844-6493)

GitHub will also show a "Cite this repository" button on the sidebar (powered by the `CITATION.cff` file).

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Development

```bash
# Clone and install in dev mode
git clone https://github.com/priya-gitTest/qrurls.git
cd qrurls
uv pip install -e ".[dev]"

# Run tests
pytest

# Lint and format
ruff check qrurls/ tests/
ruff format qrurls/ tests/

# Type check
mypy qrurls/
```
