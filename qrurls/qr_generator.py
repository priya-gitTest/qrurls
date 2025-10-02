"""
QR Code generation functionality
"""
import qrcode
from typing import Optional, Union, Any
from pathlib import Path


class QRGenerator:
    """Generate QR codes for URLs"""
    
    def __init__(self, box_size: int = 10, border: int = 4):
        """
        Initialize QR code generator
        
        Args:
            box_size: Size of each box in pixels
            border: Border size in boxes
        """
        self.box_size = box_size
        self.border = border
    
    def generate(self, url: str, output_path: Optional[str] = None) -> Optional[Any]:
        """
        Generate QR code for a URL
        
        Args:
            url: URL to encode
            output_path: Optional path to save the QR code image
            
        Returns:
            QR code image object if output_path is None, otherwise None
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=self.box_size,
            border=self.border,
        )
        
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        if output_path:
            img.save(output_path)
            return None
        
        return img
    
    def generate_svg(self, url: str) -> str:
        """
        Generate QR code as SVG string
        
        Args:
            url: URL to encode
            
        Returns:
            SVG string representation of QR code
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=self.box_size,
            border=self.border,
        )
        
        qr.add_data(url)
        qr.make(fit=True)
        
        # Generate SVG
        factory = qrcode.image.svg.SvgPathImage
        img = qr.make_image(image_factory=factory)
        
        return img.to_string(encoding='unicode')