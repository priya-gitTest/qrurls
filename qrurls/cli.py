"""
Command-line interface for qrurls
"""

import argparse
import sys
from typing import Optional, Sequence

from . import __version__
from .core import QRURLs
from .exceptions import InvalidURLError, QRUrlsError, ShorteningError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qrurls",
        description="Generate QR codes and shorten URLs from the command line",
    )
    parser.add_argument("--version", action="version", version=f"qrurls {__version__}")
    parser.add_argument("url", help="URL to process")
    parser.add_argument(
        "-s",
        "--service",
        choices=["tinyurl", "isgd", "vgd"],
        default="tinyurl",
        help="URL shortening service (default: tinyurl)",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="Output file path for QR image (default: auto-generated)",
    )
    parser.add_argument(
        "--box-size",
        type=int,
        default=10,
        help="QR code box size in pixels (default: 10)",
    )
    parser.add_argument(
        "--border",
        type=int,
        default=4,
        help="QR code border size in boxes (default: 4)",
    )

    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--shorten-only",
        action="store_true",
        help="Only shorten the URL, no QR code",
    )
    action.add_argument(
        "--qr-only",
        action="store_true",
        help="Only generate QR code, no shortening",
    )
    action.add_argument(
        "--no-qr",
        action="store_true",
        help="Alias for --shorten-only",
    )

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    shorten_only = args.shorten_only or args.no_qr

    try:
        qrurls = QRURLs(
            service=args.service,
            box_size=args.box_size,
            border=args.border,
        )

        if shorten_only:
            short_url = qrurls.shorten_only(args.url)
            print(short_url)

        elif args.qr_only:
            filepath = qrurls.qr_only(args.url, args.output)
            # Print ASCII QR to terminal
            qrurls.qr_generator.print_ascii(args.url)
            print(f"\nSaved: {filepath}")

        else:
            # Both: shorten + QR
            short_url, filepath = qrurls.process(args.url, args.output)
            # Print ASCII QR for the shortened URL
            qrurls.qr_generator.print_ascii(short_url)
            print(f"\n{short_url}")
            print(f"Saved: {filepath}")

    except InvalidURLError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ShorteningError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except QRUrlsError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
