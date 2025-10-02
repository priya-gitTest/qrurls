"""
Example usage of qrurls package
"""
from qrurls import QRURLs, QRGenerator, URLShortener


def main():
    print("=== QRURLs Examples ===\n")
    
    # Example 1: Combined functionality
    print("1. Shorten URL and generate QR code (auto filename with timestamp):")
    qrurls = QRURLs(service='tinyurl')
    short_url,filename1  = qrurls.process(
        'https://www.github.com/priya-gitTest/qrurls')
    print(f"   Original: https://www.github.com/priya-gitTest/qrurls")
    print(f"   Shortened: {short_url}")
    print(f"   QR code saved as: {filename1}\n")
    
    # Example 2: With custom filename
    print("2. Shorten URL and generate QR code (custom filename):")
    short_url, _ = qrurls.process(
        'https://opensource.org/data-governance-open-source-ai',
        output_path='osi_qr.png'
    )
    print(f"   Shortened: {short_url}")
    print(f"   QR code saved to: osi_qr.png\n")

    # Example 3: Just URL shortening
    print("3. URL shortening only:")
    shortener = URLShortener(service='isgd')
    short = shortener.shorten('https://opensource.org/data-governance-open-source-ai')
    print(f"   Original: https://opensource.org/data-governance-open-source-ai")
    print(f"   Shortened: {short}\n")
    
    # Example 4: Just QR code generation with auto filename
    print("4. QR code generation with auto filename:")
    filename = qrurls.qr_only('https://opensource.org/data-governance-open-source-ai')
    print(f"   Original: https://opensource.org/data-governance-open-source-ai")
    print(f"   QR code saved as: {filename}\n")
    
    print("Done! Check the generated PNG files.")


if __name__ == "__main__":
    main()